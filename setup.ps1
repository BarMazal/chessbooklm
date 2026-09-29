# Setup script for Chess AI Mentor & Stockfish Suite (Windows PowerShell)
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " ♟️  Chess AI Mentor & Stockfish Suite Setup" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Check Python version
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[!] Error: Python is not installed or not added to PATH." -ForegroundColor Red
    Exit 1
}

# 2. Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "[+] Creating virtual environment 'venv'..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "[✓] Virtual environment 'venv' created." -ForegroundColor Green
} else {
    Write-Host "[✓] Virtual environment 'venv' already exists." -ForegroundColor Green
}

# 3. Check & install dependencies
$depsCheck = .\venv\Scripts\python.exe -c "
import importlib.util
reqs = ['chess', 'notebooklm', 'fastapi', 'uvicorn', 'httpx', 'pydantic', 'dotenv']
missing = [r for r in reqs if importlib.util.find_spec(r) is None]
print('MISSING' if missing else 'OK')
" 2>&1

if ($depsCheck -eq "OK") {
    Write-Host "[✓] Core dependencies and Playwright browser already satisfied." -ForegroundColor Green
} else {
    Write-Host "[+] Installing dependencies into venv..." -ForegroundColor Yellow
    .\venv\Scripts\python.exe -m pip install --upgrade pip
    .\venv\Scripts\python.exe -m pip install -r requirements.txt
    .\venv\Scripts\python.exe -m playwright install chromium

    if ($LASTEXITCODE -eq 0) {
        Write-Host "[✓] Core dependencies and Playwright browser installed successfully." -ForegroundColor Green
    } else {
        Write-Host "[!] Failed to install dependencies." -ForegroundColor Red
        Exit 1
    }
}

# 4. Download and setup local Stockfish engine if missing
$sfPath = ""
if (Test-Path "stockfish\stockfish.exe") { $sfPath = "stockfish\stockfish.exe" }
elseif (Test-Path "stockfish.exe") { $sfPath = "stockfish.exe" }

if (-not $sfPath) {
    Write-Host "[+] Downloading official Stockfish binary (x86-64 universal) from GitHub..." -ForegroundColor Yellow
    .\venv\Scripts\python.exe -c "
import os, zipfile, io, httpx
stockfish_dir = 'stockfish'
exe_path = os.path.join(stockfish_dir, 'stockfish.exe')
os.makedirs(stockfish_dir, exist_ok=True)
url = 'https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-windows-x86-64-universal.zip'
try:
    print('    Downloading from GitHub releases...')
    r = httpx.get(url, follow_redirects=True, timeout=60.0)
    if r.status_code == 200:
        print('    Extracting stockfish.exe...')
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            for item in z.namelist():
                if item.endswith('.exe'):
                    with z.open(item) as src, open(exe_path, 'wb') as dst:
                        dst.write(src.read())
                    break
        print('    Stockfish downloaded and installed to stockfish/stockfish.exe')
    else:
        print(f'    Failed to download Stockfish (HTTP {r.status_code}). Fallback to Cloud API.')
except Exception as e:
    print(f'    Stockfish download error: {e}. Fallback to Cloud API.')
"
    if (Test-Path "stockfish\stockfish.exe") {
        Write-Host "[✓] Local Stockfish engine downloaded and ready at stockfish\stockfish.exe" -ForegroundColor Green
    }
} else {
    Write-Host "[✓] Local Stockfish binary already present at $sfPath" -ForegroundColor Green
}

# 5. Initialize .env file if missing
if (-not (Test-Path ".env")) {
    Write-Host "[+] Copying .env.example to .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[✓] Created .env configuration file." -ForegroundColor Green
} else {
    Write-Host "[✓] Configuration file '.env' already exists." -ForegroundColor Green
}

# 6. NotebookLM Authentication Setup Guide
Write-Host ""
Write-Host "==================================================" -ForegroundColor Magenta
Write-Host " 🔐 Google NotebookLM Authentication Guide" -ForegroundColor Magenta
Write-Host "==================================================" -ForegroundColor Magenta
Write-Host "To link your chess books notebook from NotebookLM:" -ForegroundColor White
Write-Host ""
Write-Host " Step 1: Log in to Google NotebookLM CLI (Isolated Profile 'chessbooklm')" -ForegroundColor Yellow
Write-Host "   Run the following command in your terminal:" -ForegroundColor Gray
Write-Host "     .\venv\Scripts\notebooklm.exe --profile chessbooklm login --fresh" -ForegroundColor Cyan
Write-Host "   (This opens a fresh browser window to sign in to your Google account)" -ForegroundColor DarkGray
Write-Host ""
Write-Host " Step 2: Get your Notebook ID" -ForegroundColor Yellow
Write-Host "   1. Open https://notebooklm.google.com" -ForegroundColor Gray
Write-Host "   2. Open your chess books notebook." -ForegroundColor Gray
Write-Host "   3. Copy the ID from the URL:" -ForegroundColor Gray
Write-Host "      https://notebooklm.google.com/notebook/<YOUR_NOTEBOOK_ID>" -ForegroundColor Cyan
Write-Host ""
Write-Host " Step 3: Configure Notebook ID" -ForegroundColor Yellow
Write-Host "   Paste your Notebook ID in '.env' or select it in the App UI under AI Mentor tab." -ForegroundColor Gray
Write-Host "==================================================" -ForegroundColor Magenta

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host " Setup Complete! 🎉" -ForegroundColor Green
Write-Host " To start the server, run:" -ForegroundColor White
Write-Host "   .\run.ps1" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Green
