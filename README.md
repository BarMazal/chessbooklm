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

### 1. Run Setup Script
**Windows (PowerShell)**:
```powershell
.\setup.ps1
```

**Linux / macOS (Bash)**:
```bash
chmod +x setup.sh run.sh
./setup.sh
```

---

## 🔐 Google NotebookLM Login & Setup

To connect your custom uploaded chess books in NotebookLM to the application:

### Step 1: Authenticate with NotebookLM
Run the login command from your virtual environment:

**Windows**:
```powershell
.\venv\Scripts\notebooklm.exe login
```

**Linux / macOS**:
```bash
./venv/bin/notebooklm login
```
*This opens a browser window where you can sign in to your Google account.*

### Step 2: Get your Notebook ID
1. Open [https://notebooklm.google.com](https://notebooklm.google.com) in your browser.
2. Select your notebook containing your uploaded chess PDFs & books.
3. Look at your browser address bar and copy the ID at the end of the URL:
   `https://notebooklm.google.com/notebook/<YOUR_NOTEBOOK_ID>`

Alternatively, you can list your notebooks from the command line:
```powershell
.\venv\Scripts\notebooklm.exe list
```

### Step 3: Enter your Notebook ID in the App
- Paste your Notebook ID into `.env`:
  ```env
  NOTEBOOKLM_NOTEBOOK_ID=your-notebook-id-here
  ```
- Or enter it directly in the App UI under the **Settings** tab!

---

## 🏃 Launching the Application

**Windows**:
```powershell
.\run.ps1
```

**Linux / macOS**:
```bash
./run.sh
```

Open `http://127.0.0.1:8080` in your browser.

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
├── setup.ps1 / setup.sh      # One-click installation & setup scripts
└── run.ps1 / run.sh          # Server launcher scripts
```
