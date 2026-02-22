#!/usr/bin/env bash
set -euo pipefail

echo "=== Estado de procesos ==="
ps -ef | grep -E "Codigo/Bookmarkss/server_ollama.py|Codigo/Bookmarkss/extension/server.py" | grep -v grep || echo "No hay procesos activos."

echo
echo "=== Validación de extensión (Chrome) ==="
if find "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/extension" -type d -name '__pycache__' | grep -q .; then
	echo "⚠️ Se detectó __pycache__ dentro de la extensión (Chrome puede bloquearla)."
	find "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/extension" -type d -name '__pycache__'
else
	echo "OK: no hay __pycache__ dentro de la extensión."
fi

echo
echo "=== Puertos 5000 y 6000 ==="
ss -ltnp | grep -E ':5000|:6000' || echo "Ningún puerto activo en 5000/6000."

echo
echo "=== Últimas líneas de logs ==="
echo "--- /tmp/server_ollama.log ---"
tail -n 20 /tmp/server_ollama.log 2>/dev/null || echo "Log no encontrado."

echo
echo "--- /tmp/extension_server.log ---"
tail -n 20 /tmp/extension_server.log 2>/dev/null || echo "Log no encontrado."
