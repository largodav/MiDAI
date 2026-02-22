from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sys
from datetime import datetime
from urllib import request as urlrequest
from urllib.error import URLError, HTTPError

sys.dont_write_bytecode = True

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKMARKS_FILE = os.path.join(BASE_DIR, "biblioteca_marcadores.json")
OLLAMA_SYNC_URL = os.getenv("OLLAMA_SYNC_URL", "http://localhost:6060/recibir_todos")

SERVER_STATE = {
    "status": "STARTING",
    "bookmark_count": 0,
    "updates_received": 0,
    "last_update": None,
}


def imprimir_estado_server(evento):
    print(
        "[EXT-SERVER] "
        f"evento={evento} | "
        f"status={SERVER_STATE['status']} | "
        f"marcadores={SERVER_STATE['bookmark_count']} | "
        f"updates={SERVER_STATE['updates_received']} | "
        f"last_update={SERVER_STATE['last_update']}",
        flush=True,
    )


def reenviar_a_server_ollama(marcadores):
    payload = {"marcadores": marcadores}
    req = urlrequest.Request(
        OLLAMA_SYNC_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlrequest.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {"ok": True, "data": data}
    except HTTPError as e:
        detalle = e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else str(e)
        return {"ok": False, "error": f"HTTP {e.code}: {detalle}"}
    except URLError as e:
        return {"ok": False, "error": f"No se pudo conectar con server_ollama: {e.reason}"}
    except Exception as e:
        return {"ok": False, "error": f"Error inesperado al reenviar: {str(e)}"}

@app.route('/recibir_todos', methods=['POST'])
def recibir_todos():
    datos = request.get_json(silent=True) or {}
    marcadores = datos.get('marcadores')
    if marcadores is None:
        marcadores = datos.get('bookmarks', [])

    if not isinstance(marcadores, list):
        return jsonify({"error": "El campo 'marcadores' o 'bookmarks' debe ser una lista."}), 400
    
    # Guardar todos los marcadores en un archivo JSON local
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
        json.dump(marcadores, f, ensure_ascii=False, indent=4)

    SERVER_STATE["bookmark_count"] = len(marcadores)
    SERVER_STATE["updates_received"] += 1
    SERVER_STATE["last_update"] = datetime.now().isoformat(timespec="seconds")

    sync_result = reenviar_a_server_ollama(marcadores)
    if sync_result["ok"]:
        print(f"🔁 Marcadores reenviados a server_ollama ({OLLAMA_SYNC_URL})", flush=True)
    else:
        print(f"⚠️ No se pudo reenviar a server_ollama: {sync_result['error']}", flush=True)
    
    print(f"✅ ¡Éxito! Se han recibido y guardado {len(marcadores)} marcadores.", flush=True)
    imprimir_estado_server("BOOKMARKS_UPDATED")
    return jsonify({
        "status": "recibidos",
        "total": len(marcadores),
        "server_status": SERVER_STATE,
        "sync_server_ollama": sync_result,
    }), 200


@app.route('/status', methods=['GET'])
def status_server():
    return jsonify({
        "server_status": SERVER_STATE,
        "bookmarks_file": BOOKMARKS_FILE,
        "ollama_sync_url": OLLAMA_SYNC_URL,
    }), 200

if __name__ == '__main__':
    SERVER_STATE["status"] = "RUNNING"
    if os.path.exists(BOOKMARKS_FILE):
        try:
            with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    SERVER_STATE["bookmark_count"] = len(data)
        except (json.JSONDecodeError, OSError):
            pass
    imprimir_estado_server("SERVER_START")
    app.run(host='0.0.0.0', port=5000)