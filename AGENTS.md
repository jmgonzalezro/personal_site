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

## Traducción al inglés (posts/en/)

- Mismo nombre de fichero que el español (`posts/en/Tmux_Esenciales.md`): así el
  slug y la URL no cambian. `date:` idéntica; se traduce `title:` (y `subtitle:`
  si existe). La ruta ya resuelve sola, no toques `app.py`.
- **No se traduce**: bloques y comandos, rutas de imagen, URLs, `{marginnote}`,
  ni los términos que el original ya usa en inglés (prefix, hotkeys,
  enshittification, windows/panes). Mismo número de headings, imágenes, captions
  y marginnotes, en el mismo orden.
- **No se portan las erratas** ni los coloquialismos rotos del original
  (arrunió, widnow, atrack): el inglés se escribe correcto.
- **La voz es del autor, no del traductor**:
  - tuteo → `you`; primera persona para las anécdotas propias.
  - Párrafos largos encadenados con conectores (Y, Pero, Es lo mismo que →
    And, But, It's the same thing as), nunca troceados en bullets.
  - Cierre en frases cortas declarativas ("En conclusión. Que no siempre…").
  - Registro alto y crudeza en el mismo texto, sin suavizar uno ni otro.
  - Preguntas y dudas del autor entre paréntesis, tal cual ("(unlink?)").
- **Localismos**: se conserva la idea, no la palabra. "que la ropa te dure 2
  telediarios" → "that your clothes last you two news cycles". Nada de notas al
  pie ni traducción literal; si es dudoso se marca en el commit para revisión.
- Antes de dar por bueno un post: arrancar la app y recorrer `/` y el post con
  la cookie `lang=en`, y volver a ES para comprobar que el español no cambió.

## Estructura

- `app.py` único módulo. Rutas: `/` (índice con **todos** los posts, del más
  reciente al más antiguo; scroll, sin paginación),
  `/posts/<slug>`, `/cv-terminal`. `/debug/posts` devuelve 404 a propósito.
- `templates/`: `index.html`, `post.html`, `terminal.html` (demo de ML).
- CSS: `static/css/base.css` es el propio; `tufte*`, `font-awesome*`,
  `fot-awesome*` son de terceros: no editar.

## Demo de entrenamiento en /cv-terminal

- `terminal.html` **no es el CV** (se eliminó el intérprete de comandos con el
  CV; el dueño decidirá cómo ponerlo en el web en el futuro). Ahora reproduce
  un "vídeo" ASCII de `static/neural.py`: una MLP real (2-16-1, tanh +
  sigmoid, entropía cruzada, Adam, solo stdlib) aprendiendo una espiral de dos
  brazos. Cada frame es un dashboard: mapa de decisión con los puntos del
  dataset, curva de loss, accuracy y métricas.
- La web no entrena nada: Python pregenera los frames y se sirven estáticos.
  Si tocas `neural.py`, regenera y commitea ambos JSON:
  `python static/neural.py --size 76x24 --web static/data/neural-desktop.json`
  `python static/neural.py --size 44x36 --web static/data/neural-mobile.json`
- El mismo script corre en la terminal del visitante (por eso vive en
  `static/`, accesible por URL):
  `curl -fsSL <dominio>/static/neural.py | python3` (sin args → entrena y
  reproduce en bucle; `--preview N` imprime un frame y sale).
- El JSON comprime los frames con zlib+base64; la web los abre con
  `DecompressionStream('deflate')` y colorea por carácter (`o` y `x` son las
  dos clases; el resto, la rampa del contorno). El `<pre>` usa `line-height: 1`
  y la geometría asume celdas de 0.6 x 1 em: si cambias una, cambia la otra
  (`--char-height` en el script).
