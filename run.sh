#!/bin/bash

echo "[+] Checking for available port..."
PORT=$(./venv/bin/python -c "
import socket, os
pref = int(os.getenv('PORT', '8080'))
for p in [pref, 8081, 8000, 8082, 8085]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', p))
            print(p)
            break
    except OSError:
        pass
")

if [ -z "$PORT" ]; then
    PORT=8080
fi

echo "♟️ Starting Chess AI Mentor server at http://127.0.0.1:$PORT ..."
export PYTHONPATH=$(pwd)
./venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port $PORT
