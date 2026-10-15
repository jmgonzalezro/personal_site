# Despliegue en PythonAnywhere

Todo se escribe y se despliega **desde local**. Git (GitHub) es la fuente de
verdad para control de versiones; PythonAnywhere recibe los archivos por su
API oficial y se recarga sola. No hace falta abrir la consola del navegador
ni SSH.

```
local: escribir → commit + push a GitHub → subir cambios por API → web app recargada
```

## Configuración inicial (solo una vez)

1. Genera un token: <https://www.pythonanywhere.com/account/#api_token>
   (en `eu.pythonanywhere.com` si tu cuenta es europea).

2. Crea tu `.env` (está en `.gitignore`, nunca se sube):

   ```bash
   cp .env.example .env
   # edita .env: PA_USERNAME y PA_TOKEN
   ```

3. Comprueba la conexión y descubre dominio/directorio:

   ```bash
   ./scripts/deploy.sh --check
   ```

   Imprime `PA_DOMAIN=` y `PA_DIR=` para pegarlos en `.env` (opcional, pero
   así no se descubre en cada deploy).

## Flujo diario (bloguear)

Todo desde local, un solo comando:

```bash
./scripts/nuevo_post.sh "Título del post"   # crea posts/Titulo.md con frontmatter
nvim posts/Titulo_del_post.md               # escribir
./scripts/deploy.sh "Mensaje del commit"    # commit + push + subir + recargar
```

`deploy.sh` solo sube los archivos cambiados desde el último deploy (guarda el
SHA en `.deploy_last_sha`). Flags útiles:

- `--full` — sube todos los archivos (ignora el SHA anterior). Útil tras un
  `git clone` nuevo o si sospechas de desfase.
- `--check` — valida token/usuario y muestra dominio y directorio sin desplegar.

## Notas

- La API de PythonAnywhere tiene límite de 40 peticiones/minuto; el script
  hace throttle y reintentos automáticos.
- Los borrados locales se replican en el servidor (los posts que borres
  desaparecen de la web).
- Si algún día tienes cuenta de pago, el flujo alternativo sería SSH +
  `git pull` directo; con este script no hace falta.
