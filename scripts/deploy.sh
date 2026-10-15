#!/usr/bin/env bash
# Deploy 100% desde local: commit + push a GitHub + subir los cambios a
# PythonAnywhere por su API + recargar la web app. No hace falta abrir
# la consola del navegador.
#
# Uso:
#   ./scripts/deploy.sh "Mensaje del commit"
#   ./scripts/deploy.sh --full "Mensaje"    # sube todos los archivos, no solo los cambios
#   ./scripts/deploy.sh --check             # comprueba token/usuario/dominio sin desplegar
#
# Configuración (una sola vez): crea .env copiando .env.example y rellenalo.
set -euo pipefail

cd "$(dirname "$0")/.."

# ---------------------------------------------------------------- configuración
if [[ -f .env ]]; then
    # shellcheck disable=SC1091
    source .env
fi

PA_HOST="${PA_HOST:-www.pythonanywhere.com}"
PA_USERNAME="${PA_USERNAME:-}"
PA_TOKEN="${PA_TOKEN:-}"
PA_DOMAIN="${PA_DOMAIN:-}"
PA_DIR="${PA_DIR:-}"

MODE="normal"
COMMIT_MSG=""
for arg in "$@"; do
    case "$arg" in
        --full)  MODE="full" ;;
        --check) MODE="check" ;;
        *)       COMMIT_MSG="${COMMIT_MSG:+$COMMIT_MSG }$arg" ;;
    esac
done

die() { echo "ERROR: $*" >&2; exit 1; }

[[ -n "$PA_USERNAME" ]] || die "Falta PA_USERNAME en .env (tu usuario de PythonAnywhere)."
[[ -n "$PA_TOKEN" ]]    || die "Falta PA_TOKEN en .env (pega el token de tu página de Account → API Token)."

API="https://${PA_HOST}/api/v0/user/${PA_USERNAME}"
AUTH=(-H "Authorization: Token ${PA_TOKEN}")

# ---------------------------------------------------------------- httphelpers
BODY_FILE="$(mktemp)"
trap 'rm -f "$BODY_FILE"' EXIT

# pa_request METODO URL [args de curl...] -> imprime el código HTTP
pa_request() {
    local method="$1" url="$2"
    shift 2
    curl -s -o "$BODY_FILE" -w '%{http_code}' -X "$method" "${AUTH[@]}" "$@" "$url"
}

# Límite de la API: 40 peticiones/minuto. Ventana de 60s con margen.
_window_start=0
_count=0
throttle() {
    local now
    now=$(date +%s)
    if (( now - _window_start >= 60 )); then
        _window_start=$now
        _count=0
    fi
    _count=$((_count + 1))
    if (( _count >= 35 )); then
        local wait=$(( _window_start + 60 - now ))
        if (( wait > 0 )); then
            sleep "$wait"
        fi
        _window_start=$(date +%s)
        _count=0
    fi
}

# petición con reintentos ante 429/5xx -> imprime el código HTTP
pa_request_retry() {
    local attempt code
    for attempt in 1 2 3; do
        code=$(pa_request "$@")
        case "$code" in
            429|5??) sleep $(( attempt * 15 )) ;;
            *)       echo "$code"; return 0 ;;
        esac
    done
    echo "$code"
}

# ---------------------------------------------------------------- autodescubrimiento
discover_webapp() {
    echo "Buscando tu web app en ${PA_HOST}..." >&2
    local code
    code=$(pa_request GET "${API}/webapps/")
    [[ "$code" == "200" ]] || die "La API no responde (código ${code}). ¿Token y usuario correctos? Detalle: $(cat "$BODY_FILE")"

    PA_DOMAIN=$(grep -o '"domain_name": *"[^"]*"' "$BODY_FILE" | head -1 | sed 's/.*: *"//; s/"//')
    [[ -n "$PA_DOMAIN" ]] || die "No hay ninguna web app asociada a la cuenta ${PA_USERNAME}."
    echo "Web app: ${PA_DOMAIN}" >&2

    if [[ -z "$PA_DIR" ]]; then
        # El archivo WSGI apunta al directorio real del proyecto
        code=$(pa_request GET "${API}/files/path/var/www/${PA_DOMAIN}_wsgi.py")
        if [[ "$code" == "200" ]]; then
            PA_DIR=$(grep -o "/home/${PA_USERNAME}/[^'\"]*" "$BODY_FILE" | head -1)
        fi
        PA_DIR="${PA_DIR:-/home/${PA_USERNAME}/personal_site}"
        echo "Directorio del proyecto: ${PA_DIR}" >&2
    fi
}

if [[ -z "$PA_DOMAIN" || -z "$PA_DIR" || "$MODE" == "check" ]]; then
    discover_webapp
    if [[ "$MODE" == "check" ]]; then
        echo "OK. Añade esto a tu .env para evitar el descubrimiento:"
        echo "PA_DOMAIN=${PA_DOMAIN}"
        echo "PA_DIR=${PA_DIR}"
        exit 0
    fi
fi

# ---------------------------------------------------------------- git: commit y push
if [[ -n "$(git status --porcelain)" ]]; then
    [[ -n "$COMMIT_MSG" ]] || die 'Hay cambios sin commitear: pasa un mensaje, p. ej. ./scripts/deploy.sh "Nuevo post"'
    git add -A
    git commit -m "$COMMIT_MSG"
else
    echo "No hay cambios locales; se despliega el estado actual."
fi
git push origin main

# ---------------------------------------------------------------- qué subir
LAST_FILE=".deploy_last_sha"
last="$(cat "$LAST_FILE" 2>/dev/null || true)"

uploads=()
deletes=()

if [[ "$MODE" == "full" || -z "$last" ]] || ! git cat-file -e "$last" 2>/dev/null; then
    echo "Sincronización completa (no hay SHA anterior registrado)."
    while IFS= read -r f; do
        uploads+=("$f")
    done < <(git ls-files)
else
    while IFS=$'\t' read -r status old new; do
        case "$status" in
            A*|M*|C*) uploads+=("$old") ;;
            D)        deletes+=("$old") ;;
            R*)       deletes+=("$old"); uploads+=("$new") ;;
        esac
    done < <(git diff --name-status "$last" HEAD)
fi

if [[ ${#uploads[@]} -eq 0 && ${#deletes[@]} -eq 0 ]]; then
    echo "Nada que subir a PythonAnywhere."
    exit 0
fi

echo "Subiendo ${#uploads[@]} archivo(s), borrando ${#deletes[@]}..."

status_ok=1
for f in "${deletes[@]:-}"; do
    [[ -n "$f" ]] || continue
    throttle
    code=$(pa_request_retry DELETE "${API}/files/path${PA_DIR}/${f}")
    if [[ "$code" == "204" || "$code" == "404" ]]; then
        echo "  borrado: $f"
    else
        echo "  FALLO al borrar $f (código ${code}): $(cat "$BODY_FILE")" >&2
        status_ok=0
    fi
done

for f in "${uploads[@]:-}"; do
    [[ -n "$f" ]] || continue
    case "$f" in
        *" "*) echo "  FALLO: ruta con espacios no soportada por la API: $f" >&2; status_ok=0; continue ;;
    esac
    throttle
    code=$(pa_request_retry POST "${API}/files/path${PA_DIR}/${f}" -F "content=@${f}")
    if [[ "$code" == "200" || "$code" == "201" ]]; then
        echo "  subido: $f"
    else
        echo "  FALLO al subir $f (código ${code}): $(cat "$BODY_FILE")" >&2
        status_ok=0
    fi
done

[[ "$status_ok" == "1" ]] || die "Hubo fallos de subida; no recargo la web app y no guardo el SHA."

# ---------------------------------------------------------------- recarga
throttle
code=$(pa_request_retry POST "${API}/webapps/${PA_DOMAIN}/reload/")
if [[ "$code" == "200" ]]; then
    echo "Web app recargada."
else
    # endpoint alternativo (API v1) por si cambia el v0
    throttle
    code=$(pa_request_retry POST "https://${PA_HOST}/api/v1/user/${PA_USERNAME}/websites/${PA_DOMAIN}/reload/")
    [[ "$code" == "200" ]] && echo "Web app recargada." || die "No pude recargar la web app (código ${code}). Recárgala a mano desde la pestaña Web."
fi

git rev-parse HEAD > "$LAST_FILE"
echo "Desplegado: $(git log -1 --oneline)"
