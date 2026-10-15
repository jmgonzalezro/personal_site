# Despliegue en PythonAnywhere

Fuente única de verdad: **Git (GitHub)**. El flujo es:

```
local: commit + push  →  PythonAnywhere: git pull + recarga
```

## Configuración inicial (solo una vez)

En la consola **Bash del navegador** de PythonAnywhere, dentro del directorio
de tu web app (la ruta exacta está en el archivo WSGI que apunta a `app.py`):

```bash
cd ~/personal_site          # ← ajusta a tu ruta real
cp -r ~/personal_site ~/personal_site_backup   # seguridad antes de tocar nada
git init
git remote add origin https://github.com/jmgonzalezro/personal_site.git
git fetch origin
git checkout -B main origin/main
```

Esto pisa el código del servidor con el de GitHub (bien, viene de rsync local)
y deja `venv/`, `__pycache__/` y demás archivos no versionados intactos.
El repo es público, así que no hace falta token para hacer pull.

## Flujo diario (bloguear)

1. Crear el post:

   ```bash
   ./scripts/nuevo_post.sh "Título del post"
   nvim posts/Título_del_post.md
   ```

2. Desplegar desde local:

   ```bash
   ./scripts/deploy.sh "Mensaje del commit"
   ```

   Hace commit (si hay cambios), push a GitHub y te imprime el comando final.

3. En la consola Bash del navegador de PythonAnywhere:

   ```bash
   cd ~/personal_site && ./scripts/deploy_server.sh
   ```

   Baja el último commit y recarga la web app (toca el archivo WSGI).
   Recarga la pestaña del navegador y listo.

## Si algún día tienes cuenta de pago (SSH)

Con `ssh-copy-id usuario@ssh.pythonanywhere.com` puedes ejecutar el paso 3
directamente desde local:

```bash
ssh usuario@ssh.pythonanywhere.com 'cd ~/personal_site && ./scripts/deploy_server.sh'
```

## Nota sobre rsync

Se puede seguir usando, pero si lo haces, hazlo **después** del commit+push y
con estos flags para no dejar basura ni páginas fantasma:

```bash
rsync -avz --delete \
  --exclude '.git/' --exclude 'venv/' --exclude '__pycache__/' \
  ./ usuario@ssh.pythonanywhere.com:~/personal_site/
```
