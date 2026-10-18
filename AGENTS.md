# AGENTS.md

Web personal: backend Flask de un solo fichero (`app.py`) que sirve entradas de
blog escritas en Markdown en `posts/`. No hay tests, lint, CI ni fichero de
dependencias: no inventes comandos de verificación que no existen.

## Ejecutar localmente

```bash
python3 -m venv venv
./venv/bin/pip install flask python-frontmatter markdown   # dependencias sin declarar en ningún sitio
./venv/bin/python app.py                                   # debug=False, 127.0.0.1:5000
```

El shebang de `app.py` es `#!/venv/bin/python3` (ruta absoluta inexistente
aquí, es del servidor). Localmente ejecuta siempre con `./venv/bin/python`.

Verificación mínima tras un cambio: arrancar la app y recorrer la ruta afectada.

## Flujo habitual (publicar)

```bash
./scripts/nuevo_post.sh "Título del post"   # crea posts/Titulo.md con frontmatter
# editar el .md
./scripts/deploy.sh "Mensaje del commit"    # commit + push + subir a PythonAnywhere + recargar
```

- `deploy.sh` necesita `.env` (copia de `.env.example`). `.env` y
  `.deploy_last_sha` son gitignored: **nunca** los commitees.
- Si hay cambios sin commitear, falla si no le pasas mensaje de commit.
- `--check` valida credenciales y descubre `PA_DOMAIN`/`PA_DIR`; `--full`
  fuerza subida completa (útil tras clone nuevo o si el SHA está desfasado).
- Solo sube ficheros de git: un fichero que `.gitignore` excluya nunca llega
  al servidor. `.deploy_last_sha` marca hasta dónde se subió; borrarlo obliga
  a una subida completa.
- Los borrados locales se replican en el servidor en el siguiente deploy.
- `DEPLOY.md` documenta el flujo completo y está al día (verificado contra
  `scripts/deploy.sh`). La API de PA limita 40 peticiones/min; el script ya
  hace throttle y reintentos.

## Escribir posts

- Frontmatter `title:` y `date:` en **todos** los posts (`nuevo_post.sh` ya
  los pone). Sin `date:`, `/` falla al ordenar: mezcla `datetime.date` del YAML
  con `datetime.datetime` de fallback.
- El slug es el nombre del fichero sin `.md`, literal en la URL
  (`/posts/Tmux_Esenciales`): los guiones bajos se conservan. Renombrar un
  fichero cambia su URL.
- Imágenes propias en `static/images/`, referenciadas desde los posts como
  `../static/images/foo.png` (relativo a `/posts/<slug>`). Ojo: varias imágenes
  que referencia `posts/Dead_Internet_Theory.md` (granja_bots, terminal_ai,
  dark_industry) solo existen en el servidor, no en el repo.
- Markup propio: `{marginnote}...{/marginnote}` se convierte a
  `<span class="marginnote">` antes de pasar por Markdown (extensiones
  `extra` + footnotes).
- Versión inglesa opcional: fichero con el **mismo nombre** en `posts/en/`.
  Si no existe, se sirve el español sin romper nada.

## Interfaz bilingüe (ES/EN)

- Cadenas en el dict `TRANSLATIONS` de `app.py`; las plantillas las usan como
  `t.<clave>`. Una clave nueva hay que añadirla en `es` y en `en`.
- El idioma vive en la cookie `lang` (botón EN/ES). El CV (`terminal.html`)
  está solo en español a propósito: no lo traduzcas.

## Estructura

- `app.py` único módulo. Rutas: `/` (índice paginado, 5 por página),
  `/posts/<slug>`, `/cv-terminal`. `/debug/posts` devuelve 404 a propósito.
- `templates/`: `index.html`, `post.html`, `terminal.html` (CV).
- CSS: `static/css/base.css` es el propio; `tufte*`, `font-awesome*`,
  `fot-awesome*` son de terceros: no editar.
