# ==============================================================================
#  CHESSBOOKLM - OPERATIONS MANUAL & HELP SCRIPT
# ==============================================================================
#  Usage:
#    .\help.ps1                        # Displays the complete manual
#    .\help.ps1 -Topic Servers         # Server start & kill instructions
#    .\help.ps1 -Topic NotebookLM      # NotebookLM authentication & CLI setup
#    .\help.ps1 -Topic Operation       # How to use & navigate the web application
#    .\help.ps1 -Topic Architecture    # Dual-Engine review (Stockfish + NotebookLM)
#    .\help.ps1 -CheckStatus           # Checks if backend server is currently running
#    .\help.ps1 -KillServers           # Immediately terminates any running servers
# ==============================================================================

param (
    [ValidateSet("All", "Servers", "NotebookLM", "Operation", "Architecture", "Quick")]
    [string]$Topic = "All",
    [switch]$KillServers,
    [switch]$CheckStatus
)

[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# --- Quick Action: Check Server Status ---
if ($CheckStatus) {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host " [?] Checking ChessBookLM Server Status" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan

    $ports = @(8080, 8081, 8000, 8082, 8085)
    $found = $false
    foreach ($p in $ports) {
        $conns = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
        if ($conns) {
            foreach ($c in $conns) {
                if ($c.State -eq "Listen") {
                    $proc = Get-Process -Id $c.OwningProcess -ErrorAction SilentlyContinue
                    Write-Host (" [*] Port " + $p + " is ACTIVE (PID: " + $c.OwningProcess + ", Name: " + $proc.ProcessName + ")") -ForegroundColor Green
                    Write-Host ("     Access Web UI at: http://127.0.0.1:" + $p) -ForegroundColor White
                    $found = $true
                }
            }
        }
    }

    $uvicornProcs = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn backend.main:app*" }
    if ($uvicornProcs) {
        foreach ($up in $uvicornProcs) {
            Write-Host (" [*] Active Uvicorn Backend Process found (PID: " + $up.ProcessId + ")") -ForegroundColor Green
        }
    } elseif (-not $found) {
        Write-Host " [o] No ChessBookLM server is currently listening on ports 8080/8081/8000." -ForegroundColor Yellow
        Write-Host "     Start it anytime with: .\run.ps1" -ForegroundColor Gray
    }
    Write-Host ""
    exit 0
}

# --- Quick Action: Kill Running Servers ---
if ($KillServers) {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host " [X] Stopping ChessBookLM Backend Servers" -ForegroundColor Red
    Write-Host "================================================================" -ForegroundColor Red

    $killedCount = 0

    # 1. Kill by target ports
    $targetPorts = @(8080, 8081, 8000, 8082, 8085)
    foreach ($p in $targetPorts) {
        $conns = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
        if ($conns) {
            foreach ($c in $conns) {
                $pidToKill = $c.OwningProcess
                if ($pidToKill -and $pidToKill -ne 0 -and $pidToKill -ne $PID) {
                    Write-Host (" [!] Terminating process on port " + $p + " (PID: " + $pidToKill + ")...") -ForegroundColor Yellow
                    Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
                    $killedCount++
                }
            }
        }
    }

    # 2. Kill by specific uvicorn commandline match
    $uvicornProcs = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn backend.main:app*" }
    if ($uvicornProcs) {
        foreach ($up in $uvicornProcs) {
            Write-Host (" [!] Terminating Uvicorn process (PID: " + $up.ProcessId + ")...") -ForegroundColor Yellow
            Stop-Process -Id $up.ProcessId -Force -ErrorAction SilentlyContinue
            $killedCount++
        }
    }

    Start-Sleep -Seconds 1
    if ($killedCount -gt 0) {
        Write-Host (" [OK] Successfully terminated " + $killedCount + " server process(es).") -ForegroundColor Green
    } else {
        Write-Host " [i] No active ChessBookLM server processes were found running." -ForegroundColor Gray
    }
    Write-Host ""
    exit 0
}

# --- Full Manual Functions ---

function Show-Header {
    Write-Host ""
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "        CHESSBOOKLM - COMPREHENSIVE OPERATIONS & HELP MANUAL           " -ForegroundColor Cyan
    Write-Host "      Stockfish 16 Engine + Google NotebookLM Grounded Chess Tutor     " -ForegroundColor DarkCyan
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Architecture {
    Write-Host "========================================================================" -ForegroundColor Magenta
    Write-Host " 1. DUAL-ENGINE ARCHITECTURE & HOW THE APP WORKS" -ForegroundColor Magenta
    Write-Host "========================================================================" -ForegroundColor Magenta
    Write-Host "ChessBookLM unites engine computation with book-grounded LLM mentoring:" -ForegroundColor Gray
    Write-Host ""
    Write-Host " [A] LOCAL STOCKFISH 16 ENGINE (UCI / python-chess)" -ForegroundColor Yellow
    Write-Host "     - Location : .\stockfish\stockfish.exe (auto-installed via .\setup.ps1)" -ForegroundColor White
    Write-Host "     - Function : Computes real-time centipawn (+1.25) or mate (M4) evaluations," -ForegroundColor White
    Write-Host "                  top 3 candidate moves (Multi-PV), and live tactical arrows." -ForegroundColor White
    Write-Host "     - Bot Play : Powers the interactive computer opponent with adjustable ELO" -ForegroundColor White
    Write-Host "                  (400 - 2400) and realistic blunder simulation at lower tiers." -ForegroundColor White
    Write-Host "     - Fallback : Seamlessly falls back to Lichess Cloud Eval API or heuristic" -ForegroundColor White
    Write-Host "                  material evaluation if the local binary is absent." -ForegroundColor White
    Write-Host ""
    Write-Host " [B] DETERMINISTIC CHESS TRANSLATOR (backend\chess_translator.py)" -ForegroundColor Yellow
    Write-Host "     - The bridge between raw chess math and natural-language AI reasoning." -ForegroundColor White
    Write-Host "     - Converts FEN, move history, pins, forks, loose pieces, pawn structure," -ForegroundColor White
    Write-Host "       and king safety into rich human descriptions before sending to LLM." -ForegroundColor White
    Write-Host "     - Completely eliminates the coordinate hallucinations typical of raw LLMs." -ForegroundColor White
    Write-Host ""
    Write-Host " [C] GOOGLE NOTEBOOKLM MENTOR (backend\mentor.py via notebooklm-py)" -ForegroundColor Yellow
    Write-Host "     - Isolated : Uses dedicated project profile 'chessbooklm' so credentials" -ForegroundColor White
    Write-Host "                  never collide with other local applications." -ForegroundColor White
    Write-Host "     - Grounded : Connects to your Google NotebookLM notebook uploaded with chess" -ForegroundColor White
    Write-Host "                  books, opening repertoires, GM game analyses, and PDF sources." -ForegroundColor White
    Write-Host "     - Citations: Returns strategic explanations with direct book & page citations." -ForegroundColor White
    Write-Host "     - Fallback : Includes a built-in heuristic chess strategy engine so the app" -ForegroundColor White
    Write-Host "                  is 100% functional even before authenticating with Google." -ForegroundColor White
    Write-Host ""
}

function Show-Servers {
    Write-Host "========================================================================" -ForegroundColor Green
    Write-Host " 2. HOW TO START AND KILL SERVERS" -ForegroundColor Green
    Write-Host "========================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host " ▶ HOW TO START THE SERVER:" -ForegroundColor Yellow
    Write-Host "   1. Recommended Launcher Script (Auto-resolves port & launches app):" -ForegroundColor White
    Write-Host "      .\run.ps1" -ForegroundColor Cyan
    Write-Host "      (Defaults to port 8080. If busy, checks 8081, 8000, 8082, 8085)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   2. Manual Start with Live Auto-Reload (Development Mode):" -ForegroundColor White
    Write-Host "      .\venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8080 --reload" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   3. Launch in Separate Background Window:" -ForegroundColor White
    Write-Host '      Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd ''$PWD''; .\run.ps1"' -ForegroundColor Cyan
    Write-Host ""
    Write-Host " ▶ ACCESSING THE APPLICATION:" -ForegroundColor Yellow
    Write-Host "   - Web Application UI  : http://127.0.0.1:8080" -ForegroundColor Cyan
    Write-Host "   - Interactive API Docs: http://127.0.0.1:8080/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host " ⏹ HOW TO KILL / STOP THE SERVER:" -ForegroundColor Red
    Write-Host "   1. Interactive Terminal:" -ForegroundColor White
    Write-Host "      Press Ctrl + C in the running server window." -ForegroundColor Gray
    Write-Host ""
    Write-Host "   2. Instant Kill via This Help Script:" -ForegroundColor White
    Write-Host "      .\help.ps1 -KillServers" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   3. Kill by Target Port (8080):" -ForegroundColor White
    Write-Host '      Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }' -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   4. Kill Uvicorn Process Safely (PowerShell):" -ForegroundColor White
    Write-Host '      Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -like "*uvicorn backend.main:app*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }' -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   5. Stop all Python processes (broad):" -ForegroundColor White
    Write-Host "      Stop-Process -Name python -Force -ErrorAction SilentlyContinue" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   6. Check Server Status Anytime:" -ForegroundColor White
    Write-Host "      .\help.ps1 -CheckStatus" -ForegroundColor Cyan
    Write-Host ""
}

function Show-NotebookLM {
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host " 3. NOTEBOOKLM CONNECTION & SETUP COMMAND LINES" -ForegroundColor Cyan
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "All NotebookLM CLI commands use the isolated profile '--profile chessbooklm'." -ForegroundColor Gray
    Write-Host "This ensures independent credentials that never overwrite other apps." -ForegroundColor Gray
    Write-Host ""
    Write-Host " Step 1: Sign In to Google Account (Interactive Browser Login)" -ForegroundColor Yellow
    Write-Host "   Run this command in your PowerShell terminal:" -ForegroundColor White
    Write-Host "   .\venv\Scripts\notebooklm.exe --profile chessbooklm login --fresh" -ForegroundColor Cyan
    Write-Host "   (This launches a clean browser window to sign in to your Google Account)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host " Step 2: Verify Connection Status" -ForegroundColor Yellow
    Write-Host "   .\venv\Scripts\notebooklm.exe --profile chessbooklm doctor" -ForegroundColor Cyan
    Write-Host "   (Confirms authentication status, profile name, and token validity)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host " Step 3: List Available Notebooks in Your Account" -ForegroundColor Yellow
    Write-Host "   .\venv\Scripts\notebooklm.exe --profile chessbooklm list" -ForegroundColor Cyan
    Write-Host "   (Lists your notebooks with their titles and unique Notebook IDs)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host " Step 4: Link Your Chess Notebook to ChessBookLM" -ForegroundColor Yellow
    Write-Host "   - Option A (Recommended): Open the Web UI, go to the right sidebar" -ForegroundColor White
    Write-Host "     (AI Mentor tab) and select your notebook from the dropdown list." -ForegroundColor White
    Write-Host "   - Option B (.env file): Add or update your Notebook ID in .env:" -ForegroundColor White
    Write-Host "     NOTEBOOKLM_NOTEBOOK_ID=your-notebook-uuid-here" -ForegroundColor Cyan
    Write-Host ""
    Write-Host " Step 5: Test a Grounded Query from Terminal (Optional)" -ForegroundColor Yellow
    Write-Host '   .\venv\Scripts\notebooklm.exe --profile chessbooklm ask -n <NOTEBOOK_ID> "What are the key plans in the Berlin Defense?"' -ForegroundColor Cyan
    Write-Host ""
    Write-Host " Additional CLI Utilities:" -ForegroundColor Yellow
    Write-Host "   - List all local profiles: .\venv\Scripts\notebooklm.exe profile list" -ForegroundColor Gray
    Write-Host "   - Logout current profile : .\venv\Scripts\notebooklm.exe --profile chessbooklm auth logout" -ForegroundColor Gray
    Write-Host "   - Import cookies (manual): .\venv\Scripts\notebooklm.exe --profile chessbooklm auth import-cookies cookies.json" -ForegroundColor Gray
    Write-Host ""
}

function Show-Operation {
    Write-Host "========================================================================" -ForegroundColor Yellow
    Write-Host " 4. HOW TO OPERATE THE APPLICATION" -ForegroundColor Yellow
    Write-Host "========================================================================" -ForegroundColor Yellow
    Write-Host "The application uses a 3-pane layout designed for active practice & study:" -ForegroundColor Gray
    Write-Host ""
    Write-Host " [1] CENTER PANE: INTERACTIVE CHESSBOARD & CONTROLS" -ForegroundColor White
    Write-Host "     - Piece Movement    : Click or drag pieces to make legal moves." -ForegroundColor Gray
    Write-Host "     - Stockfish Arrows  : Dynamic arrows display best move & engine threats." -ForegroundColor Gray
    Write-Host "     - Vertical Eval Bar : Shows live centipawn advantage or mate distance." -ForegroundColor Gray
    Write-Host "     - Play vs Bot Mode  : Toggle Bot on/off, adjust ELO rating (400 - 2400)." -ForegroundColor Gray
    Write-Host "     - Action Toolbar    : New Game, Flip Board, Undo Move, Reset Board." -ForegroundColor Gray
    Write-Host "     - PGN & FEN Tools   : Import/export PGN files or set custom FEN strings." -ForegroundColor Gray
    Write-Host ""
    Write-Host " [2] LEFT SIDEBAR: ENGINE ANALYSIS & CUSTOMIZATION" -ForegroundColor White
    Write-Host "     - Analysis Tab      : Live score (+0.8), ECO Opening (e.g. Italian Game)," -ForegroundColor Gray
    Write-Host "                           top 3 engine candidate lines, and PGN move table." -ForegroundColor Gray
    Write-Host "     - Settings Tab      : Board theme (11 wood, marble, slate textures)," -ForegroundColor Gray
    Write-Host "                           23 piece sets (Cburnett, Neo, Alpha, 3D, Staunton)," -ForegroundColor Gray
    Write-Host "                           sound FX, and auto-coaching move frequency." -ForegroundColor Gray
    Write-Host "     - History Tab       : Review past played games, results, and accuracy." -ForegroundColor Gray
    Write-Host ""
    Write-Host " [3] RIGHT SIDEBAR: AI MENTOR (NOTEBOOKLM)" -ForegroundColor White
    Write-Host "     - Live Coaching     : Real-time commentary tailored to your move and" -ForegroundColor Gray
    Write-Host "                           your specific student weakness profile." -ForegroundColor Gray
    Write-Host "     - Ask Mentor Chat   : Ask custom tactical or strategic questions." -ForegroundColor Gray
    Write-Host '     - Mode Switcher     : Toggle "Deterministic (Humanized)" vs "Raw FEN"' -ForegroundColor Gray
    Write-Host "                           to compare NotebookLM response quality." -ForegroundColor Gray
    Write-Host '     - Square Analysis   : Click "Deep LLM Square Analysis" for board badges' -ForegroundColor Gray
    Write-Host "                           highlighting weaknesses, outposts, and pin axes." -ForegroundColor Gray
    Write-Host "     - Turn Checklist    : Tactical alerts for hanging pieces & king safety." -ForegroundColor Gray
    Write-Host ""
    Write-Host " [4] TOP HEADER BAR: PROFILE & ANALYTICS" -ForegroundColor White
    Write-Host '     - Profile Badge     : Click "Player (ELO)" to view concept ratings matrix.' -ForegroundColor Gray
    Write-Host "     - Analytics Button  : Open adaptive training exercises for weak areas." -ForegroundColor Gray
    Write-Host "     - Status Dots       : Green/Orange dots show Engine & NotebookLM status." -ForegroundColor Gray
    Write-Host ""
}

function Show-QuickSummary {
    Write-Host "========================================================================" -ForegroundColor White
    Write-Host " 5. QUICK START CHEAT SHEET" -ForegroundColor White
    Write-Host "========================================================================" -ForegroundColor White
    Write-Host "  1. Setup dependencies  : .\setup.ps1" -ForegroundColor Yellow
    Write-Host "  2. Google sign-in      : .\venv\Scripts\notebooklm.exe --profile chessbooklm login --fresh" -ForegroundColor Yellow
    Write-Host "  3. Start the server    : .\run.ps1" -ForegroundColor Green
    Write-Host "  4. Open in browser     : http://127.0.0.1:8080" -ForegroundColor Cyan
    Write-Host "  5. Check server status : .\help.ps1 -CheckStatus" -ForegroundColor Gray
    Write-Host "  6. Stop the server     : .\help.ps1 -KillServers" -ForegroundColor Red
    Write-Host "========================================================================" -ForegroundColor White
    Write-Host ""
}

# --- Router ---
Show-Header

switch ($Topic) {
    "Servers"      { Show-Servers }
    "NotebookLM"   { Show-NotebookLM }
    "Operation"    { Show-Operation }
    "Architecture" { Show-Architecture }
    "Quick"        { Show-QuickSummary }
    Default {
        Show-Architecture
        Show-Servers
        Show-NotebookLM
        Show-Operation
        Show-QuickSummary
    }
}
