#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || (cd "$SCRIPT_DIR/../.." && pwd))"

SERVER_OLLAMA="$ROOT/Codigo/Bookmarkss/server_ollama.py"
SERVER_EXTENSION="$ROOT/Codigo/Bookmarkss/extension/server.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 no está instalado o no está en PATH."
  exit 1
fi

pkill -f "Codigo/Bookmarkss/server_ollama.py|Codigo/Bookmarkss/extension/server.py" || true

PYTHONDONTWRITEBYTECODE=1 nohup python3 "$SERVER_OLLAMA" >/tmp/server_ollama.log 2>&1 &
PID_OLLAMA=$!

PYTHONDONTWRITEBYTECODE=1 nohup python3 "$SERVER_EXTENSION" >/tmp/extension_server.log 2>&1 &
PID_EXTENSION=$!

sleep 1

echo "Servidores iniciados"
echo "- server_ollama.py PID: $PID_OLLAMA (http://127.0.0.1:6000)"
echo "- extension/server.py PID: $PID_EXTENSION (http://127.0.0.1:5000)"
echo "Logs: /tmp/server_ollama.log y /tmp/extension_server.log"
