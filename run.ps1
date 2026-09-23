# Launcher script for Chess AI Mentor (Windows PowerShell)

Write-Host "[+] Checking for existing server processes on port 8080..." -ForegroundColor Yellow

# 1. Find and stop any process listening on port 8080
$port = 8080
$connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($connections) {
    foreach ($conn in $connections) {
        $pidToKill = $conn.OwningProcess
        if ($pidToKill -and $pidToKill -ne 0) {
            Write-Host "[!] Stopping existing process (PID $pidToKill) on port $port..." -ForegroundColor Yellow
            Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
        }
    }
}

# 2. Kill any leftover uvicorn processes running backend.main:app
Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn backend.main:app*" } | ForEach-Object {
    Write-Host "[!] Stopping uvicorn process (PID $($_.ProcessId))..." -ForegroundColor Yellow
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 1

Write-Host "♟️ Starting Chess AI Mentor server at http://127.0.0.1:8080 ..." -ForegroundColor Green

$env:PYTHONPATH = (Get-Location).Path
.\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8080
