#!/usr/bin/env bash
# Uso: ./scripts/nuevo_post.sh "Título del post"
# Crea posts/<titulo_con_guiones_bajos>.md con frontmatter listo para editar.
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ $# -lt 1 || -z "$1" ]]; then
    echo 'Uso: ./scripts/nuevo_post.sh "Título del post"' >&2
    exit 1
fi

slug="${1// /_}"
file="posts/${slug}.md"

if [[ -e "$file" ]]; then
    echo "Ya existe: $file" >&2
    exit 1
fi

cat > "$file" <<EOF
---
title: "$1"
date: $(date +%F)
---

# $1

Escribe aquí tu entrada.
EOF

echo "Creado: $file"
