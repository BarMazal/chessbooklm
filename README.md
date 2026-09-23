# ♟️ Chess AI Mentor & Stockfish Suite

An interactive web-based chess application featuring real-time Stockfish engine analysis, a deterministic chess-to-human translation engine (`python-chess`), and an AI Chess Tutor powered by **Google NotebookLM** (`notebooklm-py`).

---

## 🌟 Key Features

1. **Interactive Web Interface**:
   - Classic green & cream board layout with move highlighting.
   - Live **Stockfish Move Arrows** drawn dynamically on the board.
   - Dynamic **Vertical Evaluation Bar** showing centipawn & mate advantage.
   - PGN Move History table & ECO opening detection (e.g. *Ruy Lopez: Berlin Defense*).

2. **Deterministic Chess Translator (`python-chess`)**:
   - Translates FEN, move history, tactical threats, pawn structure, and engine evaluations into natural human language.
   - **Translator Mode Switcher**: Easily test **Deterministic (Humanized)** vs **Raw FEN Mode** to compare NotebookLM's response quality.

3. **NotebookLM Integration (`notebooklm-py`)**:
   - Connects directly to your Google NotebookLM notebook loaded with chess books, grandmaster games, and tactical manuals.
   - Smart fallback strategy engine so the app works instantly before linking your NotebookLM ID.

4. **Resilient Engine Analysis**:
   - Auto-detects local `stockfish.exe` executables.
   - Gracefully falls back to the **Lichess Cloud Evaluation API** if no local Stockfish binary is installed.

---

## 🚀 Quick Setup & Installation

### Windows (PowerShell)
```powershell
# 1. Run setup script (creates venv & installs dependencies)
.\setup.ps1

# 2. Run application
.\run.ps1
```

### Linux / macOS (Bash)
```bash
# 1. Run setup script
chmod +x setup.sh run.sh
./setup.sh

# 2. Run application
./run.sh
```

---

## ⚙️ Configuration

Open `http://127.0.0.1:8080` in your browser. Navigate to the **Settings** tab in the right panel to:
- Enter your **Google NotebookLM Notebook ID**.
- Optionally set a custom path to a local Stockfish binary.

---

## 📁 Project Structure

```
chessbooklm/
├── backend/
│   ├── chess_engine.py       # Stockfish UCI & Lichess Cloud API manager
│   ├── chess_translator.py   # Deterministic chess-to-human translation engine
│   ├── config.py             # System configuration
│   ├── main.py               # FastAPI application & endpoints
│   └── mentor.py             # NotebookLM service wrapper (notebooklm-py)
├── frontend/
│   ├── index.html            # Main web UI
│   ├── styles.css            # Chessboard & dashboard styles
│   └── app.js                # Board rendering, move stack, & SVG arrows
├── requirements.txt          # Python dependencies
├── setup.ps1 / setup.sh      # One-click installation scripts
└── run.ps1 / run.sh          # Server launcher scripts
```
