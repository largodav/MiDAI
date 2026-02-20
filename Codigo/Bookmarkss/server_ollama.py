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

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKMARKS_FILE = os.path.join(BASE_DIR, "biblioteca_marcadores.json")
EXTENSION_BOOKMARKS_FILE = os.path.join(BASE_DIR, "extension", "biblioteca_marcadores.json")


def cargar_marcadores():
    rutas = [BOOKMARKS_FILE, EXTENSION_BOOKMARKS_FILE]
    for ruta in rutas:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    return []


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
    
    print(f"✅ ¡Éxito! Se han recibido y guardado {len(marcadores)} marcadores.")
    return jsonify({"status": "recibidos", "total": len(marcadores)}), 200

def consultar_ollama(prompt, modelo=None):
    payload = {
        "model": modelo or OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    req = urlrequest.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlrequest.urlopen(req, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {"ok": True, "respuesta": data.get("response", "")}
    except HTTPError as e:
        detalle = e.read().decode("utf-8", errors="ignore") if hasattr(e, "read") else str(e)
        return {"ok": False, "error": f"HTTP {e.code}: {detalle}"}
    except URLError as e:
        return {"ok": False, "error": f"No se pudo conectar con Ollama: {e.reason}"}
    except Exception as e:
        return {"ok": False, "error": f"Error inesperado: {str(e)}"}


@app.route('/preguntar_ollama', methods=['POST'])
def preguntar_ollama():
    datos = request.get_json(silent=True) or {}
    pregunta = datos.get("pregunta", "").strip()
    modelo = datos.get("modelo")
    incluir_marcadores = datos.get("incluir_marcadores", True)

    if not pregunta:
        return jsonify({"error": "Debes enviar el campo 'pregunta'."}), 400

    prompt = pregunta
    marcadores = []
    if incluir_marcadores:
        marcadores = cargar_marcadores()
        contexto = json.dumps(marcadores, ensure_ascii=False, indent=2)
        prompt = (
            "Usa estos marcadores como contexto para responder. "
            "Si no alcanzan, dilo claramente.\n\n"
            f"Marcadores:\n{contexto}\n\n"
            f"Pregunta: {pregunta}"
        )

    resultado = consultar_ollama(prompt, modelo=modelo)
    if not resultado["ok"]:
        return jsonify({"error": resultado["error"]}), 502

    return jsonify({
        "modelo": modelo or OLLAMA_MODEL,
        "marcadores_usados": len(marcadores),
        "respuesta": resultado["respuesta"],
    }), 200

if __name__ == '__main__':
    app.run(port=6000)
    