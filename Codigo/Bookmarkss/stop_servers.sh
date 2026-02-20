#!/usr/bin/env bash
set -euo pipefail

pkill -f "Codigo/Bookmarkss/server_ollama.py|Codigo/Bookmarkss/extension/server.py" || true
sleep 0.5

echo "Procesos detenidos (si estaban activos)."
ps -ef | grep -E "Codigo/Bookmarkss/server_ollama.py|Codigo/Bookmarkss/extension/server.py" | grep -v grep || true
