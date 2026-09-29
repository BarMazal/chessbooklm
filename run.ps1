# Launcher script for Chess AI Mentor (Windows PowerShell)
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "[+] Checking for available port..." -ForegroundColor Yellow

$portStr = .\venv\Scripts\python.exe -c "
import socket, os
pref = int(os.getenv('PORT', '8080'))
for p in [pref, 8081, 8000, 8082, 8085]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', p))
            print(p)
            break
    except OSError:
        pass
"

$port = 8080
if ($portStr -and [int]::TryParse($portStr.Trim(), [ref]$port)) {
    # Port resolved
} else {
    $port = 8080
}

Write-Host "[+] Stopping existing process on port $port..." -ForegroundColor Yellow

$connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($connections) {
    foreach ($conn in $connections) {
        $pidToKill = $conn.OwningProcess
        if ($pidToKill -and $pidToKill -ne 0 -and $pidToKill -ne $PID) {
            Write-Host "[!] Stopping existing process (PID $pidToKill) on port $port..." -ForegroundColor Yellow
            Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
        }
    }
}

Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn backend.main:app*" } | ForEach-Object {
    Write-Host "[!] Stopping uvicorn process (PID $($_.ProcessId))..." -ForegroundColor Yellow
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 1

Write-Host "♟️ Starting Chess AI Mentor server at http://127.0.0.1:$port ..." -ForegroundColor Green

$env:PYTHONPATH = (Get-Location).Path
.\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port $port
