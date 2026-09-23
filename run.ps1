# Launcher script for Chess AI Mentor (Windows PowerShell)

Write-Host "♟️ Starting Chess AI Mentor server at http://127.0.0.1:8080 ..." -ForegroundColor Green

$env:PYTHONPATH = (Get-Location).Path
.\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8080
