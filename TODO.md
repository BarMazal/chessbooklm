# ♟️ Chess AI Mentor & Stockfish Suite — Roadmap & TODO

This document tracks completed features, active capabilities, and planned future enhancements for the **Chess AI Mentor & Stockfish Suite**.

---

## ✅ Completed Features

### 1. Engine & Setup Architecture
- [x] **Local Stockfish Integration**: Automatic download script (`setup.ps1` / `setup.sh`) with fallback to Lichess Cloud API.
- [x] **Smart Port Handling**: Automatic detection and fallback when port `8080` is in use or blocked.
- [x] **PowerShell Compatibility**: Preserved UTF-8 with BOM encoding for PowerShell 5.1 compatibility.

### 2. Game Settings & Visual Customization
- [x] **Evaluation Score Bar**: Toggleable vertical score bar with live winning probability percentage.
- [x] **Best Move Hint Arrows**: Separate show/hide toggles for White and Black suggestion arrows.
- [x] **Player Movement Modes**: Per-color player selection (**🧑 Manual / Player** vs **🤖 Auto / Computer**).
- [x] **Toolbar Quick Actions**: Persistent "Show Hint" and "Pause / Resume" buttons.

### 3. Smart Undo Logic
- [x] **Mode-Aware Enable/Disable**: Disabled in Computer vs Computer games; enabled when at least one player is Manual.
- [x] **Context-Aware Move Reversal**:
  - **Human vs Human**: Undoes 1 move.
  - **Human vs Computer**: Undoes 1 move if Human played last; undoes 2 moves (Computer response + preceding Human move) if Computer played last.

### 4. Stockfish Difficulty Levels
- [x] **Skill Level Integration**: Native Stockfish UCI `Skill Level` (0 to 20) via `/api/board/bot-move`.
- [x] **Dynamic Rating Badges**: Labels mapping skill levels to ELO ratings (`Beginner / Casual (~1300 ELO)` to `Grandmaster / Max (~3000+ ELO)`).
- [x] **Independent Computer Tiers**: White and Black can play with different difficulty levels in Computer vs Computer mode.
- [x] **Disabled State Styling**: Sliders marked disabled when a side is set to Player.
- [x] **Auto-Pause on Settings**: Game automatically pauses when opening Game Settings.

### 5. Interactive Board Editor (`✏️ Edit Board`)
- [x] **Piece Palette Bar**: Two-row SVG piece selector (White & Black), Active Turn toggle, Clear Board, Standard Setup, and Remove Tool.
- [x] **Drag & Drop / Touch Placement**: Add, move, replace, or remove pieces directly on the board.
- [x] **King Count Validation**: Ensures exactly 1 White King and 1 Black King before applying positions.
- [x] **5 Configurable Warning Alerts**: Toggles in Game Settings for Overriding Piece, Removing Piece, Check, Checkmate, and Stalemate/Tie.
- [x] **Engine Recognition**: Calculates Stockfish evaluations and candidate moves for custom positions without breaking game flow.
- [x] **Auto-Pause & Toggle**: Automatically pauses when entering Edit Mode and hides palette outside Edit Mode.

### 6. Save & Load Games, FEN & PGN Utilities
- [x] **Save & Load Games Library**: Persist current games to browser local storage with custom titles and notes.
- [x] **Direct FEN Import/Export**: View, copy, or load custom position FEN strings directly.
- [x] **PGN Export & Import**: Download game PGN files, copy PGN to clipboard, or import external PGNs.
- [x] **Copy Move History**: One-click button to copy current move sequence in SAN notation.

### 7. User Profiles, ELO Tracking & Skill Assessment Matrix
- [x] **Compact Persistent Header Item**: Displays `[👤 Profile Name | 📈 ELO]` in top navbar without cluttering board real estate.
- [x] **Multi-User Profile Management**: Non-persistent modal to create, switch, or delete multiple user profiles with starting skill levels.
- [x] **Concept-Based Skill Breakdown**: Tracks rating/progress across 6 strategic concepts (Offensive Strategy, Defensive Maneuvers, Tactics & Forks, Battery Attacks, Pins & Skewers, Endgame & Gambits).
- [x] **Rating System Conversions**: Displays equivalent ratings across major systems (FIDE, USCF, Chess.com Blitz, Lichess Classical, ECF).
- [x] **Auto-Adjust Computer Difficulty**: Dynamically matches Stockfish strength to active profile ELO with Challenge Tiers (🟢 Easy, 🟡 Medium, 🟠 Hard, 🔴 Nightmare).
- [x] **AI Mentor Placement Test**: Step-by-step diagnostic test powered by live Lichess Open Puzzle API & Stockfish-calibrated situations.

### 8. Chess Clocks & Time Controls
- [x] **Dual Digital Clock Display**: Integrated active turn header clocks for ⚪ White and ⚫ Black near the board.
- [x] **Standard & Custom Time Control Presets**: Supports ⚡ Blitz (3+2, 5+0), ⏱️ Rapid (10+0, 15+10), ⏳ Classical (30+0), and custom minute/increment settings.
- [x] **Independent Per-Player Time Controls (Odds Controls)**: Configure White and Black timers independently, including `♾️ Untimed / No Limit`.
- [x] **Automate Loss on Time Flag**: Option in Game Settings to trigger automatic game over at `00:00` or flag and continue.
- [x] **⚡ Force Move Button**: Instant action toolbar button to force the computer to play its move immediately.
- [x] **Smooth 100ms Precision Countdown**: Ticks down active player's clock smoothly after game starts.
- [x] **Move Increment Support**: Automatically adds increment seconds (e.g. +2s, +10s) upon move completion.
- [x] **Time Flagging & Game Over**: Automatic game end detection with glowing red card animation when clock reaches `00:00`.

### 9. Advanced AI Mentor Capabilities
- [x] **Opening Book Explorer**: Interactive ECO opening dictionary, continuation branches, and win/draw/loss percentage statistics (`📖 Opening Book`).
- [x] **Interactive Position Tutor Quizzes**: Position-based 3-option tactical and strategic quizzes generated on-demand (`🧩 Quiz`).
- [x] **Full Post-Game Move Analysis**: Stockfish evaluation graph, move classification (🌟 Brilliant, ✨ Best, 👍 Good, ⚠️ Mistake, 💥 Blunder, 📖 Book), and accuracy metrics (`🔍 Game Analysis`).
- [x] **AI Coach Post-Game Report**: Automatic narrative analysis of key turning points and actionable advice from AI Mentor / NotebookLM.

---

## 📋 Planned / Future Roadmap

### 1. Audio & Visual Polish
- [ ] **Sound Effects**: Audio feedback for move execution, captures, checks, and game end.
- [ ] **Custom Board Themes**: Choice of board color schemes (Wood, Marble, Glass, Modern Dark).
- [ ] **Custom Piece Sets**: Selection of piece sets (Neoclassic, Alpha, Merida, Staunton).

### 2. Resource-Grounded Guided Lessons & Spaced Repetition
- [ ] **Interactive Masterclass Drills**: Guided board exercise mode where student plays variations step-by-step with real-time AI Mentor coaching sourced from video/book transcripts.
- [ ] **Repetition & Realization Loops**: Student repeats drill variations until demonstrating 100% accuracy and conceptual understanding.
- [ ] **Student Lesson Mastery Log**: Persistence of completed lessons, accuracy stats, and skill confidence levels per opening/tactic.
- [ ] **Spaced Repetition Retention Tests**: Automated re-testing schedule (1d, 3d, 7d, 30d) to verify long-term memory retention.

### 3. Per-Profile Concept Proficiency Analytics & ROI Report
- [ ] **Granular Element Tracking**: Track student rating and accuracy over time across specific strategic concepts (Defense, Specific Openings, Forks, Sacrifices, White vs Black performance).
- [ ] **Progress Delta Reporting**: Periodic reports detailing what skills improved, plateaued, or regressed.
- [ ] **Cost-Performance (ROI) Improvement Ranking**: Ranks recommended practice topics by ROI (high-frequency / high-impact errors prioritized first for fastest rating gains).



- [ ] Concept-Based Skill Breakdown additions
- Passed pawns, time stress (ELO under Blitz and such)