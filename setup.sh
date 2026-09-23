#!/bin/bash

echo "=================================================="
echo " ♟️  Chess AI Mentor & Stockfish Suite Setup"
echo "=================================================="

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "[!] Error: python3 could not be found."
    exit 1
fi

echo "[✓] Python 3 found: $(python3 --version)"

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "[+] Creating virtual environment 'venv'..."
    python3 -m venv venv
    echo "[✓] Virtual environment created."
fi

# Install requirements
echo "[+] Installing dependencies into venv..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Create .env if missing
if [ ! -f ".env" ]; then
    echo "[+] Creating .env from .env.example..."
    cp .env.example .env
fi

echo ""
echo "=================================================="
echo " Setup Complete! 🎉"
echo " To start the server, run:"
echo "   ./run.sh"
echo "=================================================="
