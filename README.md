# MiDAI

Coddigo

## Bookmarkss - uso diario

Guía completa: [Codigo/Bookmarkss/instrucciones.md](Codigo/Bookmarkss/instrucciones.md)

### Puertos

- `5000`: servidor de extensión (`extension/server.py`)
- `6060`: servidor web/chat (`server_ollama.py`)
- `11434`: API local de Ollama

### Comandos rápidos (WSL)

```bash
cd /ruta/a/MiDAI/Codigo/Bookmarkss
bash start_servers.sh    # iniciar ambos servidores
bash status_servers.sh   # ver estado, puertos y logs
bash stop_servers.sh     # detener servidores
```

### URLs útiles

- Chat web: `http://localhost:6060/`
- Estado extensión: `http://localhost:5000/status`
