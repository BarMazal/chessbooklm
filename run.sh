#!/bin/bash

echo "♟️ Starting Chess AI Mentor server at http://127.0.0.1:8080 ..."
export PYTHONPATH=$(pwd)
./venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8080
