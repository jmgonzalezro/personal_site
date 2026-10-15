#!/usr/bin/env bash
# Deploy desde local: commit (si hay cambios) + push a GitHub.
# Después, ejecuta en la consola Bash de PythonAnywhere:
#   cd ~/personal_site && ./scripts/deploy_server.sh
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -n "$(git status --porcelain)" ]]; then
    msg="${*:-Update $(date +%F\ %T)}"
    git add -A
    git commit -m "$msg"
else
    echo "No hay cambios locales; no se crea commit."
fi

git push origin main

echo
echo "Push hecho. Ahora, en la consola Bash de PythonAnywhere (navegador):"
echo "  cd ~/personal_site && ./scripts/deploy_server.sh"
