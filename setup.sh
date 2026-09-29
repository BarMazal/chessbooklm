#!/bin/bash

echo "=================================================="
echo " ♟️  Chess AI Mentor & Stockfish Suite Setup"
echo "=================================================="

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "[!] Error: python3 could not be found."
    exit 1
fi

echo "[✓] Found Python 3: $(python3 --version)"

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "[+] Creating virtual environment 'venv'..."
    python3 -m venv venv
    echo "[✓] Virtual environment 'venv' created."
else
    echo "[✓] Virtual environment 'venv' already exists."
fi

# Check & install dependencies
deps_check=$(./venv/bin/python -c "
import importlib.util
reqs = ['chess', 'notebooklm', 'fastapi', 'uvicorn', 'httpx', 'pydantic', 'dotenv']
missing = [r for r in reqs if importlib.util.find_spec(r) is None]
print('MISSING' if missing else 'OK')
" 2>&1)

if [ "$deps_check" = "OK" ]; then
    echo "[✓] Core dependencies and Playwright browser already satisfied."
else
    echo "[+] Installing dependencies into venv..."
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
    ./venv/bin/python -m playwright install chromium
    echo "[✓] Core dependencies installed successfully."
fi

# Download and setup local Stockfish engine if missing
sf_path=""
if [ -f "stockfish/stockfish.exe" ]; then sf_path="stockfish/stockfish.exe";
elif [ -f "stockfish/stockfish" ]; then sf_path="stockfish/stockfish";
elif command -v stockfish &> /dev/null; then sf_path="$(command -v stockfish)";
fi

if [ -z "$sf_path" ]; then
    echo "[+] Downloading official Stockfish binary from GitHub..."
    ./venv/bin/python -c "
import os, zipfile, tarfile, io, httpx, platform
stockfish_dir = 'stockfish'
os.makedirs(stockfish_dir, exist_ok=True)
system = platform.system().lower()
if 'linux' in system:
    url = 'https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-universal.tar'
    bin_name = 'stockfish'
elif 'darwin' in system:
    url = 'https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-macos-x86-64-universal.tar'
    bin_name = 'stockfish'
else:
    url = 'https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-windows-x86-64-universal.zip'
    bin_name = 'stockfish.exe'

target_path = os.path.join(stockfish_dir, bin_name)
try:
    print('    Downloading from GitHub releases...')
    r = httpx.get(url, follow_redirects=True, timeout=60.0)
    if r.status_code == 200:
        print('    Extracting binary to stockfish/...')
        if url.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                for item in z.namelist():
                    if item.endswith('.exe'):
                        with z.open(item) as src, open(target_path, 'wb') as dst:
                            dst.write(src.read())
                        break
        else:
            with tarfile.open(fileobj=io.BytesIO(r.content)) as t:
                for member in t.getmembers():
                    if member.name.endswith('stockfish') or member.name.endswith('stockfish.exe'):
                        src = t.extractfile(member)
                        if src:
                            with open(target_path, 'wb') as dst:
                                dst.write(src.read())
                            os.chmod(target_path, 0o755)
                            break
        print('    Stockfish downloaded and installed to stockfish/')
except Exception as e:
    print(f'    Stockfish download error: {e}. Fallback to Cloud API.')
"
else
    echo "[✓] Local Stockfish binary already present at $sf_path"
fi

# Create .env if missing
if [ ! -f ".env" ]; then
    echo "[+] Creating .env from .env.example..."
    cp .env.example .env
    echo "[✓] Created .env configuration file."
else
    echo "[✓] Configuration file '.env' already exists."
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
