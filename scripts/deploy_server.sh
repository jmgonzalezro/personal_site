#!/usr/bin/env bash
# Ejecutar en la consola Bash de PythonAnywhere: baja el último commit
# desde GitHub y recarga la web app tocando el archivo WSGI.
set -euo pipefail

cd "$HOME/personal_site"   # ← Ajusta si tu web app vive en otro directorio

git pull --ff-only

wsgi_file="${WSGI_FILE:-$(ls /var/www/*wsgi*.py 2>/dev/null | head -n1)}"
if [[ -z "$wsgi_file" ]]; then
    echo "No encuentro el archivo WSGI en /var/www/. No recargo la web app."
    echo "Puedes recargarla a mano desde la pestaña Web."
    exit 1
fi

touch "$wsgi_file"
echo "Desplegado. Último commit: $(git log -1 --oneline)"
echo "Web app recargada ($wsgi_file)."
