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
./venv/bin/python -m playwright install chromium

# Create .env if missing
if [ ! -f ".env" ]; then
    echo "[+] Creating .env from .env.example..."
    cp .env.example .env
fi

echo ""
echo "=================================================="
echo " 🔐 Google NotebookLM Authentication Guide"
echo "=================================================="
echo "To link your chess books notebook from NotebookLM:"
echo ""
echo " Step 1: Log in to Google NotebookLM CLI (Isolated Profile 'chessbooklm')"
echo "   Run:"
echo "     ./venv/bin/notebooklm --profile chessbooklm login --fresh"
echo "   (This opens a fresh browser window to sign in to your Google account)"
echo ""
echo " Step 2: Get your Notebook ID"
echo "   1. Open https://notebooklm.google.com"
echo "   2. Open your chess books notebook."
echo "   3. Copy the ID from the URL:"
echo "      https://notebooklm.google.com/notebook/<YOUR_NOTEBOOK_ID>"
echo ""
echo " Step 3: Configure Notebook ID"
echo "   Paste your Notebook ID in '.env' or select it in the App UI under AI Mentor tab."
echo "=================================================="

echo ""
echo "=================================================="
echo " Setup Complete! 🎉"
echo " To start the server, run:"
echo "   ./run.sh"
echo "=================================================="
