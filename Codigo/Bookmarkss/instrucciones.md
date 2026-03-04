# Instrucciones del módulo `Bookmarkss`

Este documento resume la estructura de carpetas que estamos usando en `Codigo/Bookmarkss`, cómo levantar los servidores y en qué puertos funciona cada componente.

## 1) Estructura de carpetas

```text
Codigo/Bookmarkss/
├─ biblioteca_marcadores.json        # Base local de marcadores (servidor web/chat)
├─ server_ollama.py                  # Servidor Flask para chat + integración con Ollama
├─ prueba_agentes_ollama.py          # Prueba de LangChain contra Ollama
├─ prueba_agentes_gemini.py          # Prueba de agente con Gemini
├─ start_servers.sh                  # Arranque conjunto de servidores
├─ status_servers.sh                 # Estado de procesos, puertos y logs
├─ stop_servers.sh                   # Detención de servidores
├─ extension/
│  ├─ manifest.json                  # Config de extensión (Chrome)
│  ├─ background.js                  # Lógica principal de extensión
│  ├─ server.py                      # Servidor Flask receptor/sincronizador de marcadores
│  └─ biblioteca_marcadores.json     # Copia local de marcadores desde la extensión
├─ templates/
│  └─ chat_modelo.html               # UI del chat web
└─ static/
   ├─ chat_modelo.css                # Estilos del chat
   └─ chat_modelo.js                 # Lógica frontend del chat
```

## 2) Arquitectura y flujo

1. La extensión (o cliente) envía marcadores a `extension/server.py`.
2. `extension/server.py` guarda los datos y los reenvía a `server_ollama.py`.
3. `server_ollama.py` mantiene los marcadores, expone el chat web y consulta Ollama.
4. Ollama responde desde su API local.

### Puertos involucrados

- `5000`: servidor de extensión (`extension/server.py`)
- `6060`: servidor web/chat (`server_ollama.py`)
- `11434`: API de Ollama (servicio Ollama local)

## 3) Endpoints importantes

### `server_ollama.py` (puerto 6060)

- `GET /` → interfaz web del chat
- `POST /api/chat` → endpoint principal para preguntar
- `POST /preguntar_ollama` → endpoint alternativo de consulta
- `POST /recibir_todos` → recibe y guarda todos los marcadores

### `extension/server.py` (puerto 5000)

- `POST /recibir_todos` → recibe marcadores (`marcadores` o `bookmarks`)
- `GET /status` → estado del servidor, conteo y última sincronización

## 4) Variables de entorno útiles

### En `server_ollama.py`

- `OLLAMA_URL` (default: `http://localhost:11434/api/generate`)
- `OLLAMA_MODEL` (default: `gpt-oss:20b`)
- `OLLAMA_WEB_PORT` (default: `6060`)

### En `extension/server.py`

- `OLLAMA_SYNC_URL` (default: `http://localhost:6060/recibir_todos`)

## 5) Cómo levantar los servidores

> Recomendado en terminal **WSL** desde la raíz del repo (`MiDAI`).

### 5.1 Arranque automático (ambos servidores)

```bash
cd /ruta/a/MiDAI/Codigo/Bookmarkss
bash start_servers.sh
```

Este script:

- limpia `__pycache__` de la extensión,
- mata procesos previos de ambos servidores,
- levanta ambos servicios en segundo plano,
- deja logs en:
  - `/tmp/server_ollama.log`
  - `/tmp/extension_server.log`

### 5.2 Ver estado

```bash
cd /ruta/a/MiDAI/Codigo/Bookmarkss
bash status_servers.sh
```

Valida:

- procesos activos,
- puertos `5000` y `6060`,
- últimas líneas de logs,
- presencia de `__pycache__` en extensión.

### 5.3 Detener servicios

```bash
cd /ruta/a/MiDAI/Codigo/Bookmarkss
bash stop_servers.sh
```

## 6) Verificación rápida

- Chat web: `http://localhost:6060/`
- Estado extensión: `http://localhost:5000/status`

Desde WSL también suele mostrarse una URL con IP interna (`http://<IP_WSL>:6060/`).

## 7) Requisitos mínimos

- `python3` disponible en PATH
- Paquetes Python usados por los servidores:
  - `flask`
  - `flask-cors`
- Ollama corriendo localmente para responder consultas en `11434`

Ejemplo de instalación rápida:

```bash
pip install flask flask-cors
```

Si Ollama no está activo, el chat levantará pero devolverá error al consultar modelo.
