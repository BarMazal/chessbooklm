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

if ($LASTEXITCODE -eq 0) {
    Write-Host "[✓] Dependencies installed successfully." -ForegroundColor Green
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

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host " Setup Complete! 🎉" -ForegroundColor Green
Write-Host " To start the server, run:" -ForegroundColor White
Write-Host "   .\run.ps1" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Green
