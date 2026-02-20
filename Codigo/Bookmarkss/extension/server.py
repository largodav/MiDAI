from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sys
from urllib import request as urlrequest
from urllib.error import URLError, HTTPError

sys.dont_write_bytecode = True

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKMARKS_FILE = os.path.join(BASE_DIR, "biblioteca_marcadores.json")
OLLAMA_SYNC_URL = os.getenv("OLLAMA_SYNC_URL", "http://localhost:6000/recibir_todos")


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

    sync_result = reenviar_a_server_ollama(marcadores)
    if sync_result["ok"]:
        print(f"🔁 Marcadores reenviados a server_ollama ({OLLAMA_SYNC_URL})")
    else:
        print(f"⚠️ No se pudo reenviar a server_ollama: {sync_result['error']}")
    
    print(f"✅ ¡Éxito! Se han recibido y guardado {len(marcadores)} marcadores.")
    return jsonify({
        "status": "recibidos",
        "total": len(marcadores),
        "sync_server_ollama": sync_result,
    }), 200

if __name__ == '__main__':
    app.run(port=5000)