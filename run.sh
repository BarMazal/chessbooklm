#!/bin/bash

echo "[+] Checking for existing server processes on port 8080..."

# Kill any process listening on port 8080
fuser -k 8080/tcp 2>/dev/null || true
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Kill any running uvicorn backend.main:app process
pkill -f "uvicorn backend.main:app" 2>/dev/null || true

sleep 1

echo "♟️ Starting Chess AI Mentor server at http://127.0.0.1:8080 ..."
export PYTHONPATH=$(pwd)
./venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8080
