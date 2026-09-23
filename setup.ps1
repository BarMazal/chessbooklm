# Setup script for Chess AI Mentor & Stockfish Suite (Windows PowerShell)

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
    Write-Host "[✓] Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "[✓] Virtual environment 'venv' already exists." -ForegroundColor Green
}

# 3. Activate venv & install dependencies
Write-Host "[+] Installing dependencies into venv..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pip install "notebooklm-py[browser]"

if ($LASTEXITCODE -eq 0) {
    Write-Host "[✓] Core dependencies installed successfully." -ForegroundColor Green
} else {
    Write-Host "[!] Failed to install dependencies." -ForegroundColor Red
    Exit 1
}

# 4. Initialize .env file if missing
if (-not (Test-Path ".env")) {
    Write-Host "[+] Copying .env.example to .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "[✓] Created .env configuration file." -ForegroundColor Green
}

# 5. NotebookLM Authentication Setup Guide
Write-Host ""
Write-Host "==================================================" -ForegroundColor Magenta
Write-Host " 🔐 Google NotebookLM Authentication Guide" -ForegroundColor Magenta
Write-Host "==================================================" -ForegroundColor Magenta
Write-Host "To link your chess books notebook from NotebookLM:" -ForegroundColor White
Write-Host ""
Write-Host " Step 1: Log in to Google NotebookLM CLI (Isolated Profile 'chessbooklm')" -ForegroundColor Yellow
Write-Host "   Run the following command in your terminal:" -ForegroundColor LightGray
Write-Host "     .\venv\Scripts\notebooklm.exe --profile chessbooklm login --fresh" -ForegroundColor Cyan
Write-Host "   (This opens a fresh browser window to sign in to your Google account)" -ForegroundColor Gray
Write-Host ""
Write-Host " Step 2: Get your Notebook ID" -ForegroundColor Yellow
Write-Host "   1. Open https://notebooklm.google.com" -ForegroundColor LightGray
Write-Host "   2. Open your chess books notebook." -ForegroundColor LightGray
Write-Host "   3. Copy the ID from the URL:" -ForegroundColor LightGray
Write-Host "      https://notebooklm.google.com/notebook/<YOUR_NOTEBOOK_ID>" -ForegroundColor Cyan
Write-Host ""
Write-Host " Step 3: Configure Notebook ID" -ForegroundColor Yellow
Write-Host "   Paste your Notebook ID in '.env' or select it in the App UI under AI Mentor tab." -ForegroundColor LightGray
Write-Host "==================================================" -ForegroundColor Magenta

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host " Setup Complete! 🎉" -ForegroundColor Green
Write-Host " To start the server, run:" -ForegroundColor White
Write-Host "   .\run.ps1" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Green
