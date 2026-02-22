#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || (cd "$SCRIPT_DIR/../.." && pwd))"

SERVER_OLLAMA="$ROOT/Codigo/Bookmarkss/server_ollama.py"
SERVER_EXTENSION="$ROOT/Codigo/Bookmarkss/extension/server.py"
EXTENSION_DIR="$ROOT/Codigo/Bookmarkss/extension"
PYCACHE_ROOT="/tmp/midai_pycache"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 no está instalado o no está en PATH."
  exit 1
fi

mkdir -p "$PYCACHE_ROOT"
find "$EXTENSION_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} + || true

pkill -f "Codigo/Bookmarkss/server_ollama.py|Codigo/Bookmarkss/extension/server.py" || true

PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$PYCACHE_ROOT" nohup python3 "$SERVER_OLLAMA" >/tmp/server_ollama.log 2>&1 &
PID_OLLAMA=$!

PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="$PYCACHE_ROOT" nohup python3 "$SERVER_EXTENSION" >/tmp/extension_server.log 2>&1 &
PID_EXTENSION=$!

sleep 1
WSL_IP="$(hostname -I | awk '{print $1}')"

echo "SERVIDORES INICIADOS"
echo "------SERVIDOR OLLAMA --------------------------------------"
echo "- server_ollama.py PID: $PID_OLLAMA (http://127.0.0.1:6060)"
echo "------SERVIDOR EXTENSIONES --------------------------------------"
echo "- extension/server.py PID: $PID_EXTENSION (http://127.0.0.1:5000)"
echo "------ STATUS Servidor Extensiones  --------------------------------------"
echo "Se puede consulta en http://127.0.0.1:5000/status"
echo "Logs: /tmp/server_ollama.log y /tmp/extension_server.log"
echo "Pycache redirigido a: $PYCACHE_ROOT"
echo "Chat web (Windows): http://localhost:6060/"
echo "Chat web (IP WSL): http://$WSL_IP:6060/"

HTTP_CODE_6060="$(curl -sS -m 3 -o /dev/null -w '%{http_code}' http://127.0.0.1:6060/ || echo '000')"
echo "Health 6060: $HTTP_CODE_6060"

echo
echo "=== Estado tras arranque ==="
"$SCRIPT_DIR/status_servers.sh"
