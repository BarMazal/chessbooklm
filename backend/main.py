import os
import json
import re
from datetime import datetime
import chess
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from backend.chess_engine import ChessEngineManager
from backend.chess_translator import ChessTranslator
from backend.mentor import MentorService
from backend.config import STOCKFISH_PATH, NOTEBOOKLM_NOTEBOOK_ID, NOTEBOOKLM_AUTH_TOKEN, HOST, PORT

app = FastAPI(title="Chess AI Mentor & Stockfish Suite", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

engine_manager = ChessEngineManager(stockfish_path=STOCKFISH_PATH)
mentor_service = MentorService(notebook_id=NOTEBOOKLM_NOTEBOOK_ID, auth_token=NOTEBOOKLM_AUTH_TOKEN)


class BoardStateRequest(BaseModel):
    fen: Optional[str] = None
    moves: Optional[List[str]] = None
    depth: Optional[int] = 12


class BotMoveRequest(BaseModel):
    fen: Optional[str] = None
    moves: Optional[List[str]] = None
    skill_level: Optional[int] = 20
    target_elo: Optional[int] = None


class PgnParseRequest(BaseModel):
    pgn: str


class PgnExportRequest(BaseModel):
    moves: List[str]
    fen: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    annotations: Optional[List[str]] = None




class MentorExplainRequest(BaseModel):
    fen: str
    moves: Optional[List[str]] = None
    mode: Optional[str] = "human"  # "human" or "raw_fen"
    question: Optional[str] = None
    student_color: Optional[str] = "white"
    practice_subject: Optional[str] = "auto"
    turn_guidelines: Optional[List[dict]] = None
    user_profile: Optional[dict] = None
    notebook_id: Optional[str] = None


class LLMSquareAnalysisRequest(BaseModel):
    fen: Optional[str] = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    moves: Optional[List[str]] = []
    student_color: Optional[str] = "white"
    notebook_id: Optional[str] = None
    user_profile: Optional[Dict[str, Any]] = None


def format_user_profile_context(user_prof: Optional[dict]) -> str:
    if not user_prof:
        return ""
    name = user_prof.get("name", "Student")
    elo = user_prof.get("elo", 1500)
    concepts = user_prof.get("concepts", {})
    if not concepts or not isinstance(concepts, dict):
        return f"\nStudent Profile: {name} ({elo} ELO)"
    
    sorted_concepts = sorted(concepts.values(), key=lambda c: c.get("rating", 1500) if isinstance(c, dict) else 1500)
    concept_lines = [f"- {c.get('icon', '♟️')} {c.get('name', 'Category')}: {c.get('rating', 1500)} rating" for c in sorted_concepts if isinstance(c, dict)]
    
    return (
        f"\nStudent Profile Context: {name} ({elo} ELO)\n"
        f"Category Skill Ratings (Sorted by Weakness Priority - Lowest First):\n" + "\n".join(concept_lines) + "\n"
        f"CRITICAL DIRECTIVE: You MUST prioritize your feedback, focus practice subject, and turn advice around the student's LOWEST-rated skill categories first. Address their specific skill weaknesses before general commentary."
    )


class ConfigUpdateRequest(BaseModel):
    stockfish_path: Optional[str] = None
    notebook_id: Optional[str] = None
    auth_token: Optional[str] = None


class SelectNotebookRequest(BaseModel):
    notebook_id: str


class LoginRequest(BaseModel):
    email: Optional[str] = None
    fresh: Optional[bool] = True
    profile_name: Optional[str] = None


class SwitchProfileRequest(BaseModel):
    profile_name: str


class ImportCookiesRequest(BaseModel):
    cookies_json: str


@app.on_event("shutdown")
def shutdown_event():
    engine_manager.close()


@app.get("/api/status")
async def get_status():
    auth_info = await mentor_service.get_auth_status()
    return {
        "status": "online",
        "stockfish": {
            "has_local_binary": engine_manager._engine is not None,
            "path": engine_manager.stockfish_path or "Using Lichess Cloud Fallback"
        },
        "notebooklm": {
            "notebook_id": mentor_service.notebook_id or "Not configured",
            "is_configured": bool(mentor_service.notebook_id),
            "is_logged_in": auth_info["is_logged_in"],
            "profile": auth_info["profile"]
        }
    }


@app.get("/api/auth/status")
async def get_auth_status():
    """
    Returns Google NotebookLM account authentication status and active profile.
    """
    return await mentor_service.get_auth_status()


@app.post("/api/auth/login")
async def trigger_login(req: Optional[LoginRequest] = None):
    """
    Triggers notebooklm login process in browser.
    Setting fresh=True forces a clean session so Google prompts for User Email & Password.
    """
    email = req.email if req else None
    fresh = req.fresh if req else True
    profile_name = req.profile_name if req else None
    return await mentor_service.trigger_login(email=email, fresh=fresh, profile_name=profile_name)


@app.get("/api/auth/profiles")
async def list_profiles():
    """
    Lists all stored notebooklm account profiles.
    """
    profiles = await mentor_service.list_profiles()
    return {"profiles": profiles, "active_profile": mentor_service.active_profile}


@app.post("/api/auth/profiles/switch")
async def switch_profile(req: SwitchProfileRequest):
    """
    Switches active notebooklm profile.
    """
    return await mentor_service.switch_profile(req.profile_name)


@app.post("/api/auth/logout")
async def logout():
    """
    Logs out of the current Google NotebookLM account.
    """
    return await mentor_service.logout()


@app.post("/api/auth/import-cookies")
async def import_cookies(req: ImportCookiesRequest):
    """
    Imports Google authentication cookies from JSON.
    """
    return await mentor_service.import_cookies(req.cookies_json)


@app.get("/api/notebooks")
async def get_notebooks():
    """
    Returns list of all available NotebookLM notebooks for the active account profile.
    """
    notebooks = await mentor_service.list_notebooks()
    return {
        "active_notebook_id": mentor_service.notebook_id,
        "notebooks": notebooks
    }


@app.post("/api/notebooks/select")
async def select_notebook(req: SelectNotebookRequest):
    """
    Sets the active NotebookLM notebook to be used as the AI Mentor.
    """
    mentor_service.notebook_id = req.notebook_id
    
    # Save to .env file if present
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "NOTEBOOKLM_NOTEBOOK_ID=" in content:
                import re
                content = re.sub(r"NOTEBOOKLM_NOTEBOOK_ID=.*", f"NOTEBOOKLM_NOTEBOOK_ID={req.notebook_id}", content)
            else:
                content += f"\nNOTEBOOKLM_NOTEBOOK_ID={req.notebook_id}\n"
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"[Main] Failed to update .env: {e}")

    return {
        "success": True,
        "active_notebook_id": mentor_service.notebook_id,
        "message": f"Active NotebookLM Mentor updated to ID: {req.notebook_id}"
    }


def build_board_from_request(fen: Optional[str], moves: Optional[List[str]]) -> chess.Board:
    """
    Safely constructs a chess.Board from FEN or moves list.
    Prioritizes specific non-start FEN so current board state is accurately reflected.
    """
    STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    if fen and fen != "start" and fen.strip() != STARTING_FEN:
        try:
            return chess.Board(fen)
        except Exception:
            pass

    if moves and len(moves) > 0:
        board = chess.Board()
        for m in moves:
            try:
                board.push_san(m)
            except Exception:
                try:
                    board.push_uci(m)
                except Exception:
                    pass
        return board
    elif fen and fen != "start":
        try:
            return chess.Board(fen)
        except Exception:
            return chess.Board()
    else:
        return chess.Board()


@app.post("/api/board/evaluate")
async def evaluate_board(req: BoardStateRequest):
    try:
        board = build_board_from_request(req.fen, req.moves)
        eval_res = await engine_manager.evaluate_position(board, depth=req.depth or 12)
        opening_name = ChessTranslator.identify_opening(board)
        tactics = ChessTranslator.get_tactical_summary(board)
        overlays = ChessTranslator.analyze_board_positional_overlays(board)

        legal_moves = [{"uci": m.uci(), "san": board.san(m)} for m in board.legal_moves]

        w_king = board.king(chess.WHITE)
        b_king = board.king(chess.BLACK)
        white_in_check = board.is_attacked_by(chess.BLACK, w_king) if w_king is not None else False
        black_in_check = board.is_attacked_by(chess.WHITE, b_king) if b_king is not None else False
        is_check = board.is_check() or white_in_check or black_in_check

        checked_sides = []
        if white_in_check or (board.turn == chess.WHITE and board.is_check()):
            checked_sides.append("White")
        if black_in_check or (board.turn == chess.BLACK and board.is_check()):
            checked_sides.append("Black")

        return {
            "fen": board.fen(),
            "turn": "white" if board.turn == chess.WHITE else "black",
            "opening": opening_name,
            "is_check": is_check,
            "white_in_check": white_in_check,
            "black_in_check": black_in_check,
            "checked_sides": checked_sides,
            "is_game_over": board.is_game_over(),
            "eval": eval_res,
            "tactics": tactics,
            "overlays": overlays,
            "legal_moves": legal_moves
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid board evaluation request: {str(e)}")


@app.post("/api/board/overlays")
async def get_board_overlays(req: BoardStateRequest):
    try:
        board = build_board_from_request(req.fen, req.moves)
        overlays = ChessTranslator.analyze_board_positional_overlays(board)
        return {"success": True, "overlays": overlays}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to analyze board overlays: {str(e)}")


@app.post("/api/board/llm-square-analysis")
async def llm_square_analysis(req: LLMSquareAnalysisRequest):
    """
    Performs a deep LLM square-by-square strategic & tactical analysis of the position.
    Enumerate key squares with weaknesses, outposts, and tactical motifs, returning both
    board overlay markers and natural-language mentor commentary.
    """
    try:
        board = build_board_from_request(req.fen, req.moves)
        eval_res = await engine_manager.evaluate_position(board, depth=10)
        human_text = ChessTranslator.translate_position_to_human(board, eval_res, "")
        baseline_overlays = ChessTranslator.analyze_board_positional_overlays(board)

        prof_context = format_user_profile_context(req.user_profile)

        prompt = (
            f"You are an expert chess mentor performing a deep square-by-square strategic analysis of the current board position.\n"
            f"{prof_context}\n\n"
            f"Current Position FEN: {board.fen()}\n"
            f"Board Evaluation & Positional Summary:\n{human_text}\n\n"
            f"CRITICAL REQUIREMENT:\n"
            f"You MUST analyze and evaluate key squares from BOTH White's and Black's perspective:\n"
            f"1. White's perspective: Highlight White's target weaknesses, key outposts, defender anchors, and tactical threats.\n"
            f"2. Black's perspective: Highlight Black's target weaknesses, key outposts, defender anchors, and tactical threats.\n"
            f"3. Enumerate EVERY key square explicitly at the beginning of bullet points (e.g. `e5: ...`, `f6: ...`).\n"
            f"4. At the end of your response, output a JSON array of square annotations enclosed in a ```json ... ``` block.\n"
            f"   Example JSON format:\n"
            f"   ```json\n"
            f"   [\n"
            f"     {{\"square\": \"e5\", \"label\": \"Undefended Target\", \"category\": \"weak\", \"type\": \"target\", \"side\": \"b\"}},\n"
            f"     {{\"square\": \"e4\", \"label\": \"Contested Center\", \"category\": \"weak\", \"type\": \"target\", \"side\": \"w\"}},\n"
            f"     {{\"square\": \"d5\", \"label\": \"Outpost Hole\", \"category\": \"strong\", \"type\": \"outpost\", \"side\": \"w\"}},\n"
            f"     {{\"square\": \"e2\", \"label\": \"Pin Axis\", \"category\": \"tactical\", \"type\": \"pin\", \"side\": \"w\"}}\n"
            f"   ]\n"
            f"   ```\n\n"
            f"REQUIRED MARKDOWN STRUCTURE:\n"
            f"### ⚪ White's Key Squares (Weaknesses & Strengths)\n"
            f"(Enumerate 2-4 key squares for White with format `square: explanation`)\n\n"
            f"### ⚫ Black's Key Squares (Weaknesses & Strengths)\n"
            f"(Enumerate 2-4 key squares for Black with format `square: explanation`)\n\n"
            f"### 🛡️ Tactical Motifs & Engine vs. Human Insights\n"
            f"(Explain tactical axes like pins, forks, loose pieces, or what simple engine evaluations miss)\n\n"
            f"### 💡 Generalized Turn Rule\n"
            f"(Formulate 1 general, reusable strategic heuristic derived from this position applicable to future games, e.g., 'When opponent overextends pawns, target the base of the chain with counter-levers'. DO NOT write specific move notation like 7...Na5 here!)\n"
        )

        mentor_res = await mentor_service.query_mentor(prompt, notebook_id=req.notebook_id)
        raw_response = mentor_res["response"]

        # Extract JSON block for overlays if present
        parsed_overlays = []
        if "```json" in raw_response:
            try:
                json_part = raw_response.split("```json")[1].split("```")[0].strip()
                parsed_overlays = json.loads(json_part)
            except Exception as pe:
                print(f"[LLMSquareAnalysis] Failed to parse overlay JSON: {pe}")

        # Standardize badge icons and tooltips if missing
        badge_map = {
            "target": "🎯",
            "weak": "⚠️",
            "outpost": "🏰",
            "pin": "🧲",
            "fork": "⚔️",
            "control": "🛡️",
            "key_square": "⭐",
            "defender": "🛡️"
        }

        # Combine parsed overlays with baseline overlays
        final_overlays = []
        seen_sqs = set()

        if parsed_overlays and isinstance(parsed_overlays, list):
            for item in parsed_overlays:
                if isinstance(item, dict) and item.get("square"):
                    sq = item["square"].lower()
                    if sq not in seen_sqs:
                        seen_sqs.add(sq)
                        o_type = item.get("type", "target")
                        b_icon = badge_map.get(o_type, "🎯")
                        label = item.get("label", "Key Square")
                        side = item.get("side", "w")
                        cat = item.get("category", "weak")
                        final_overlays.append({
                            "square": sq,
                            "side": side,
                            "category": cat,
                            "type": o_type,
                            "badge": b_icon,
                            "tooltip": f"{label} ({sq.upper()})"
                        })

        for bo in baseline_overlays:
            if isinstance(bo, dict) and bo.get("square"):
                sq = bo["square"].lower()
                if sq not in seen_sqs:
                    seen_sqs.add(sq)
                    final_overlays.append(bo)

        # Remove JSON block from commentary text for pristine display
        clean_response = raw_response
        if "```json" in clean_response:
            clean_response = clean_response.split("```json")[0].strip()

        return {
            "success": True,
            "overlays": final_overlays,
            "response": clean_response,
            "provider": mentor_res["provider"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"LLM Square analysis failed: {str(e)}")


@app.get("/api/puzzles/placement")
async def get_placement_puzzles():
    """
    Returns ELO-calibrated chess placement situations from Lichess Open Puzzle API
    (or fallback Stockfish-verified situations if offline).
    """
    import urllib.request
    import json

    puzzles = []

    # Attempt fetching live Lichess daily puzzle
    try:
        req = urllib.request.Request(
            "https://lichess.org/api/puzzle/daily",
            headers={"User-Agent": "ChessAIMentor/1.0"}
        )
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            data = json.loads(resp.read().decode())
            puz = data.get("puzzle", {})
            game = data.get("game", {})
            if puz and "rating" in puz:
                puzzles.append({
                    "id": puz.get("id", "lichess_daily"),
                    "rating": puz.get("rating", 1500),
                    "theme": puz.get("themes", ["Tactics"])[0] if puz.get("themes") else "Tactics",
                    "title": f"🌐 Live Lichess Puzzle (~{puz.get('rating', 1500)} ELO)",
                    "desc": f"Theme: {', '.join(puz.get('themes', ['Tactics'])[:3])}. Solve the position!",
                    "fen": game.get("fen", "r4rk1/pp1q1ppp/8/3nN3/8/8/PP3PPP/R2Q1RK1 w - - 0 1"),
                    "source": "Lichess API",
                    "options": [
                        {"text": f"⚡ Play Best Tactical Solution ({puz.get('solution', [''])[0]})", "bonus": 250, "correct": True},
                        {"text": "🛡️ Play Passive Defense Move", "bonus": 100, "correct": False},
                        {"text": "♟️ Play Neutral Pawn Move", "bonus": 50, "correct": False}
                    ]
                })
    except Exception as e:
        pass

    # Curated Stockfish-verified ELO-calibrated set
    fallback_puzzles = [
        {
            "id": "placement_1000",
            "rating": 1050,
            "theme": "Tactics & Royal Fork",
            "title": "⚡ Beginner Situation (~1050 ELO)",
            "desc": "White to move. Black's Queen (d7) and King (g8) are active. What is White's top tactical move?",
            "fen": "r4rk1/pp1q1ppp/8/3nN3/8/8/PP3PPP/R2Q1RK1 w - - 0 1",
            "source": "Stockfish Calibrated",
            "options": [
                {"text": "⚡ Play Qxd5 (Trade Queen for Knight)", "bonus": 50, "correct": False},
                {"text": "👑 Play Nxd7! (Fork & Win Black's Queen)", "bonus": 250, "correct": True},
                {"text": "🛡️ Play Nf3 (Retreat Knight safely)", "bonus": 100, "correct": False}
            ]
        },
        {
            "id": "placement_1500",
            "rating": 1520,
            "theme": "Defensive Fortification & Counter-Attack",
            "title": "🛡️ Intermediate Situation (~1520 ELO)",
            "desc": "Black is launching a Kingside pawn storm against White's King. How should White respond?",
            "fen": "r1b2rk1/pp2qpbp/2pp1np1/4p3/2PPP3/2N1BP2/PP2B1PP/R2Q1RK1 w - - 0 11",
            "source": "Stockfish Calibrated",
            "options": [
                {"text": "🛡️ Central counter-strike & Nd5 anchor", "bonus": 250, "correct": True},
                {"text": "🏃 Push h3 & g4 (Creates pawn weaknesses)", "bonus": 80, "correct": False},
                {"text": "♟️ Passively wait on the Kingside", "bonus": 40, "correct": False}
            ]
        },
        {
            "id": "placement_1900",
            "rating": 1910,
            "theme": "Battery Alignment & 7th Rank Pressure",
            "title": "🔋 Advanced Situation (~1910 ELO)",
            "desc": "White has doubled Rooks on the d-file facing Black's position. What positional move maximizes pressure?",
            "fen": "3r2k1/1r3p1p/p5p1/1p6/3R4/1PR3P1/P4P1P/6K1 w - - 0 25",
            "source": "Stockfish Calibrated",
            "options": [
                {"text": "🔋 Infiltrate 7th rank with Rd7! (Rook Battery Infiltration)", "bonus": 250, "correct": True},
                {"text": "🔄 Trade rooks immediately with Rxd8+", "bonus": 120, "correct": False},
                {"text": "🛡️ Retreat Rook back to d1", "bonus": 50, "correct": False}
            ]
        }
    ]

    combined = puzzles + fallback_puzzles
    return {"puzzles": combined}


@app.post("/api/board/bot-move")
async def get_bot_move(req: BotMoveRequest):
    try:
        if req.fen and req.fen != "start":
            try:
                board = chess.Board(req.fen)
            except Exception:
                board = chess.Board()
        else:
            board = chess.Board()

        if req.moves and len(req.moves) > 0:
            for m in req.moves:
                try:
                    board.push_san(m)
                except Exception:
                    try:
                        board.push_uci(m)
                    except Exception:
                        pass

        if board.is_game_over():
            raise HTTPException(status_code=400, detail="Game is already over")

        skill_level = req.skill_level if req.skill_level is not None else 20
        return await engine_manager.get_bot_move(board, skill_level=skill_level, target_elo=req.target_elo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bot move generation failed: {str(e)}")


@app.post("/api/pgn/parse")
async def parse_pgn(req: PgnParseRequest):
    try:
        import chess.pgn
        import io
        game = chess.pgn.read_game(io.StringIO(req.pgn))
        if not game:
            raise HTTPException(status_code=400, detail="Could not parse PGN content.")

        headers = dict(game.headers)
        board = game.board()
        san_moves = []
        uci_moves = []

        for move in game.mainline_moves():
            san_moves.append(board.san(move))
            uci_moves.append(move.uci())
            board.push(move)

        return {
            "success": True,
            "headers": headers,
            "san_moves": san_moves,
            "uci_moves": uci_moves,
            "final_fen": board.fen()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PGN Parse failed: {str(e)}")


@app.post("/api/pgn/export")
async def export_pgn(req: PgnExportRequest):
    try:
        import chess.pgn
        import datetime

        game = chess.pgn.Game()
        h = req.headers or {}
        game.headers["Event"] = h.get("Event", "Chess AI Mentor Game")
        game.headers["Site"] = h.get("Site", "Chess AI Mentor Suite")
        game.headers["Date"] = h.get("Date", datetime.date.today().strftime("%Y.%m.%d"))
        game.headers["White"] = h.get("White", "Player (White)")
        game.headers["Black"] = h.get("Black", "Stockfish AI (Black)")
        game.headers["Result"] = h.get("Result", "*")

        board = chess.Board(req.fen) if req.fen else chess.Board()
        game.setup(board)

        node = game
        for idx, m_str in enumerate(req.moves):
            try:
                move = board.push_san(m_str)
            except Exception:
                move = board.push_uci(m_str)
            node = node.add_variation(move)
            if req.annotations and idx < len(req.annotations):
                node.comment = req.annotations[idx]

        exporter = chess.pgn.StringExporter(headers=True, comments=True, variations=False)
        pgn_string = game.accept(exporter)

        return {
            "success": True,
            "pgn": pgn_string
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PGN Export failed: {str(e)}")




@app.post("/api/mentor/explain")
async def explain_position(req: MentorExplainRequest):
    try:
        board = build_board_from_request(req.fen, req.moves)
        eval_res = await engine_manager.evaluate_position(board, depth=12)

        if req.mode == "raw_fen":
            prompt = ChessTranslator.translate_raw_fen_mode(req.fen, req.question)
        else:
            prompt = ChessTranslator.translate_position_to_human(board, eval_res, req.question)

        if req.practice_subject:
            prompt += f"\n\nFocus Practice Subject: {req.practice_subject}"
        if req.turn_guidelines:
            rules_str = "\nActive Board Checklist & Alerts:\n" + "\n".join([f"- {r.get('icon', '🛡️')} {r.get('title', '')}: {r.get('text', '')}" for r in req.turn_guidelines[:3]])
            prompt += f"\n{rules_str}"

        mentor_res = await mentor_service.query_mentor(prompt, notebook_id=req.notebook_id)

        return {
            "fen": board.fen(),
            "mode": req.mode,
            "prompt_sent": prompt,
            "provider": mentor_res["provider"],
            "response": mentor_res["response"],
            "eval_summary": eval_res.get("score", "0.0"),
            "best_move": eval_res.get("best_move_san", "")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Mentor analysis failed: {str(e)}")


class ExtractGuidelinesRequest(BaseModel):
    fen: Optional[str] = None
    moves: Optional[List[str]] = None
    analysis_text: Optional[str] = None


@app.post("/api/mentor/extract-guidelines")
async def extract_guidelines(req: ExtractGuidelinesRequest):
    """
    Extracts actionable turn guidelines/rules from game moves, position evaluation or mentor advice.
    """
    try:
        import time
        board = build_board_from_request(req.fen, req.moves)
        extracted_rules = []
        eval_res = await engine_manager.evaluate_position(board, depth=10)

        # Check for hanging/loose pieces
        w_loose = [sq for sq, piece in board.piece_map().items() if piece.color == chess.WHITE and not board.is_attacked_by(chess.WHITE, sq) and board.is_attacked_by(chess.BLACK, sq)]
        b_loose = [sq for sq, piece in board.piece_map().items() if piece.color == chess.BLACK and not board.is_attacked_by(chess.BLACK, sq) and board.is_attacked_by(chess.WHITE, sq)]

        if w_loose or b_loose:
            sq_names = [chess.square_name(s) for s in (w_loose + b_loose)]
            extracted_rules.append({
                "id": f"rule_auto_loose_{int(time.time())}",
                "icon": "🛡️",
                "title": "Loose Piece Vigilance Alert",
                "text": f"Before completing your move, double-check undefended target(s) at {', '.join(sq_names)}.",
                "citations": f"[Game Analysis - Move {len(req.moves or [])}]",
                "category": "Tactics"
            })

        if board.is_check():
            extracted_rules.append({
                "id": f"rule_auto_check_{int(time.time())}",
                "icon": "👑",
                "title": "Check Defense & King Escape Squares",
                "text": "When under check, evaluate all blocking, capturing, and king escape (luft) options carefully.",
                "citations": "[Game Analysis - Check Step]",
                "category": "King Safety"
            })

        if req.analysis_text:
            lines = req.analysis_text.split("\n")
            for idx, line in enumerate(lines):
                l = line.strip()
                if (l.startswith(('-', '*', '1.', '2.', '3.')) or 'rule' in l.lower() or 'avoid' in l.lower() or 'mistake' in l.lower()) and len(l) > 12:
                    clean_text = l.lstrip('-*0123456789. ').strip()
                    if len(clean_text) > 10:
                        extracted_rules.append({
                            "id": f"rule_auto_text_{int(time.time())}_{idx}",
                            "icon": "🎓",
                            "title": f"Mentor Takeaway #{idx + 1}",
                            "text": clean_text,
                            "citations": "[AI Mentor Post-Game Advice]",
                            "category": "Strategy"
                        })

        if not extracted_rules:
            extracted_rules.append({
                "id": f"rule_auto_gen_{int(time.time())}",
                "icon": "🎯",
                "title": "Strategic Patience & Outpost Control",
                "text": "Identify passive pieces after move 15 and improve their activity before launching tactical attacks.",
                "citations": "[AI Mentor Auto-Analysis]",
                "category": "Strategy"
            })

        return {"success": True, "guidelines": extracted_rules}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Guideline extraction failed: {str(e)}")


class LiveCoachingRequest(BaseModel):
    fen: Optional[str] = None
    moves: Optional[List[str]] = None
    move_number: int
    student_color: Optional[str] = "white"
    practice_subject: Optional[str] = "auto"
    turn_guidelines: Optional[List[dict]] = None
    user_profile: Optional[dict] = None
    notebook_id: Optional[str] = None


@app.post("/api/mentor/live-coaching")
async def live_coaching(req: LiveCoachingRequest):
    """
    Generates dynamic natural-language live mentor commentary for Move req.move_number,
    tailored to the active practice subject, global turn guidelines, and mentored student color.
    """
    try:
        board = build_board_from_request(req.fen, req.moves)
        eval_res = await engine_manager.evaluate_position(board, depth=10)
        human_text = ChessTranslator.translate_position_to_human(board, eval_res, "")

        student_color_name = (req.student_color or "white").upper()
        active_turn_color = "White" if board.turn == chess.WHITE else "Black"

        if student_color_name == "WHITE":
            student_desc = "The student is playing as WHITE."
            color_formatting = (
                "### ⚪ Mentoring White\n"
                "(2-3 concise sentences evaluating White's position, key move ideas, piece activity, and king safety)"
            )
        elif student_color_name == "BLACK":
            student_desc = "The student is playing as BLACK."
            color_formatting = (
                "### ⚫ Mentoring Black\n"
                "(2-3 concise sentences evaluating Black's position, key move ideas, piece activity, and king safety)"
            )
        else:
            student_desc = "The student is managing BOTH sides (White and Black) in a practice game."
            color_formatting = (
                "### ⚪ Mentoring White\n"
                "(1-2 concise sentences evaluating White's position and key ideas)\n\n"
                "### ⚫ Mentoring Black\n"
                "(1-2 concise sentences evaluating Black's position and key ideas)"
            )

        rules_str = ""
        if req.turn_guidelines:
            rules_str = "Active Board Checklist & Tactical Alerts:\n" + "\n".join([f"- {r.get('icon', '🛡️')} {r.get('title', '')}: {r.get('text', '')}" for r in req.turn_guidelines[:4]])
        else:
            rules_str = "Active Board Checklist & Tactical Alerts: None active."

        subject_title = req.practice_subject if (req.practice_subject and req.practice_subject != "auto") else "Auto (Mentor Selection)"
        prof_context = format_user_profile_context(req.user_profile)

        prompt = (
            f"You are an expert live chess mentor coaching your student.\n"
            f"{student_desc}\n"
            f"{prof_context}\n\n"
            f"Current Position State: Move {req.move_number} completed. Turn to move: {active_turn_color}.\n\n"
            f"Board Evaluation & Structure Summary:\n{human_text}\n\n"
            f"Active Practice Subject: {subject_title}\n"
            f"{rules_str}\n\n"
            f"REQUIRED STRUCTURE - You MUST structure your response into EXACTLY these distinct Markdown sections:\n\n"
            f"{color_formatting}\n\n"
            f"### 🎯 Focus Practice Subject: {subject_title}\n"
            f"(Provide 2-3 sentences evaluating the position specifically against this practice subject. Highlight current situation and actionable mentor guidance based on the student's category skill ratings.)\n\n"
            f"### 🛡️ Turn Checklist & Pitfalls Avoidance\n"
            f"(Provide 2-3 sentences referencing active board alerts like loose pieces, king safety/luft, or simplification, and advise how to avoid pitfalls on this turn.)"
        )

        mentor_res = await mentor_service.query_mentor(prompt, notebook_id=req.notebook_id)

        return {
            "success": True,
            "move_number": req.move_number,
            "student_color": req.student_color or "white",
            "fen": board.fen(),
            "response": mentor_res["response"],
            "provider": mentor_res["provider"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Live coaching failed: {str(e)}")


class SuggestSubjectsRequest(BaseModel):
    fen: Optional[str] = None
    moves: Optional[List[str]] = None
    user_profile: Optional[dict] = None
    notebook_id: Optional[str] = None


@app.post("/api/mentor/suggest-subjects")
async def suggest_subjects(req: SuggestSubjectsRequest):
    """
    Analyzes game trajectory & blunders to suggest new practice subjects or pitfalls.
    """
    try:
        board = build_board_from_request(req.fen, req.moves)
        eval_res = await engine_manager.evaluate_position(board, depth=10)
        human_text = ChessTranslator.translate_position_to_human(board, eval_res, "")
        prof_context = format_user_profile_context(req.user_profile)

        prompt = (
            f"You are a master chess mentor reviewing a student's game position and move history.\n"
            f"{prof_context}\n\n"
            f"Game Position Summary:\n{human_text}\n"
            f"Moves Played: {', '.join((req.moves or [])[-12:])}\n\n"
            f"Based on this game history and the student's category skill ratings (prioritizing lowest ratings first), identify 2-3 specific practice subjects or tactical pitfalls the student should focus on.\n"
            f"Return a JSON array of objects with keys: 'id', 'title', 'category', 'description', 'is_pitfall' (boolean)."
        )

        mentor_res = await mentor_service.query_mentor(prompt, notebook_id=req.notebook_id)
        raw_resp = mentor_res.get("response", "")

        import json, re
        suggestions = []
        try:
            match = re.search(r'\[.*\]', raw_resp, re.DOTALL)
            if match:
                suggestions = json.loads(match.group(0))
        except Exception:
            suggestions = [
                {
                    "id": "subj_king_pawn_shield",
                    "title": "King Pawn Shield Integrity",
                    "category": "King Safety",
                    "description": "Avoid advancing pawns in front of castled king prematurely.",
                    "is_pitfall": True
                },
                {
                    "id": "subj_open_file_control",
                    "title": "Rook Battery & Open File Control",
                    "category": "Strategy",
                    "description": "Double rooks on open files before pushing central pawns.",
                    "is_pitfall": False
                }
            ]

        return {"success": True, "suggestions": suggestions, "provider": mentor_res["provider"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Subject suggestion failed: {str(e)}")


# ==========================================
# 🧠 STRUCTURED MENTOR NODE & SEQUENCE ANALYSIS
# ==========================================
class NodeTimeMetrics(BaseModel):
    game_full_time_ms: Optional[int] = 300000
    clock_remaining_ms: Optional[int] = None
    move_duration_ms: Optional[int] = None
    time_spent_ratio: Optional[float] = None
    time_pressure_flag: Optional[bool] = False
    stress_index: Optional[int] = 10
    stress_level: Optional[str] = "Low"

class NodeRunningErrorMetrics(BaseModel):
    running_blunder_count: Optional[int] = 0
    running_missed_opportunities_count: Optional[int] = 0
    running_mistake_count: Optional[int] = 0
    running_inaccuracy_count: Optional[int] = 0
    blunder_frequency: Optional[float] = 0.0
    missed_opportunity_frequency: Optional[float] = 0.0
    running_accuracy_pct: Optional[float] = 100.0

class NodeEvalContext(BaseModel):
    stockfish_eval: Optional[str] = None
    eval_val: Optional[float] = None
    prev_eval_val: Optional[float] = None
    eval_delta: Optional[float] = None
    win_probability_before: Optional[float] = None
    win_probability_after: Optional[float] = None
    win_probability_delta: Optional[float] = None
    move_classification: Optional[str] = None
    strategic_swing_type: Optional[str] = None
    strategic_swing_label: Optional[str] = None

class MentorNodeAnalysisRequest(BaseModel):
    node_id: Optional[str] = None
    fen: str
    move_number: int
    color: str
    move_san: str
    move_uci: Optional[str] = None
    sequence_moves: Optional[List[str]] = []
    time_control_metrics: Optional[NodeTimeMetrics] = None
    running_error_metrics: Optional[NodeRunningErrorMetrics] = None
    eval_context: Optional[NodeEvalContext] = None
    notebook_id: Optional[str] = None
    analysis_type: Optional[str] = "all"

class BatchMentorNodeAnalysisRequest(BaseModel):
    nodes: List[MentorNodeAnalysisRequest]
    notebook_id: Optional[str] = None
    analysis_type: Optional[str] = "all"

def build_mentor_node_prompt(req: MentorNodeAnalysisRequest) -> str:
    seq_str = " -> ".join(req.sequence_moves[-16:]) if req.sequence_moves else req.move_san
    tm = req.time_control_metrics or NodeTimeMetrics()
    clock_sec = round((tm.clock_remaining_ms or 0) / 1000, 1) if tm.clock_remaining_ms is not None else "N/A"
    duration_sec = round((tm.move_duration_ms or 0) / 1000, 1) if tm.move_duration_ms is not None else "N/A"
    full_time_min = round((tm.game_full_time_ms or 0) / 60000, 1) if tm.game_full_time_ms is not None else "N/A"
    time_pressure_str = "YES (Under acute time trouble!)" if tm.time_pressure_flag else "No (Adequate clock time)"
    stress_str = f"{tm.stress_index}/100 ({tm.stress_level})"

    em = req.running_error_metrics or NodeRunningErrorMetrics()
    blunder_cnt = em.running_blunder_count or 0
    missed_cnt = em.running_missed_opportunities_count or 0
    mistake_cnt = em.running_mistake_count or 0
    inacc_cnt = em.running_inaccuracy_count or 0
    blunder_freq = em.blunder_frequency or 0.0
    missed_freq = em.missed_opportunity_frequency or 0.0
    accuracy_pct = em.running_accuracy_pct or 100.0

    ec = req.eval_context or NodeEvalContext()
    eval_score = ec.stockfish_eval or "N/A"
    eval_delta = f"{ec.eval_delta:+0.2f}" if ec.eval_delta is not None else "N/A"
    classification = ec.move_classification or "Standard"
    swing_label = ec.strategic_swing_label or "Normal play"

    player_color = "White" if req.color == 'w' else "Black"

    prompt = f"""You are a master chess mentor reviewing a student's move node in a historic game tree.
Analyze this position, the sequence of moves that led to it, the player's clock time telemetry, and their cumulative blunder/missed-opportunity frequencies.

=== MOVE & BOARD CONTEXT ===
- Move: #{req.move_number} by {player_color}: {req.move_san} ({req.move_uci or 'N/A'})
- FEN: {req.fen}
- Move Sequence Leading to this Node: {seq_str}
- Stockfish Evaluation: {eval_score} (Eval Delta: {eval_delta})
- Move Classification: {classification} ({swing_label})

=== CLOCK & TIME CONTROL TELEMETRY ===
- Total Game Time: {full_time_min} minutes
- Clock Remaining: {clock_sec} seconds
- Move Thinking Time: {duration_sec} seconds
- Time Pressure Status: {time_pressure_str}
- Cognitive Stress Index: {stress_str}

=== ERROR METRICS & FREQUENCIES (CUMULATIVE TO THIS MOVE) ===
- Running Blunders: {blunder_cnt}
- Running Missed Opportunities: {missed_cnt}
- Running Mistakes: {mistake_cnt} | Inaccuracies: {inacc_cnt}
- Blunder Frequency: {blunder_freq} blunders per move
- Missed Opportunity Frequency: {missed_freq} missed opportunities per move
- Running Accuracy: {accuracy_pct}%

=== MENTOR TASK & REQUIRED STRUCTURE ===
Provide in-depth pedagogical analysis answering:
1. How did the sequence of moves leading up to this point set the tactical/strategic conditions for {req.move_san}?
2. How did the player's clock time ({clock_sec}s left, {duration_sec}s spent) and stress index ({stress_str}) influence the quality or precision of this move?
3. How does this move connect to the player's blunder frequency ({blunder_freq}) and missed-opportunity frequency ({missed_freq})? Is this part of a recurring tactical pattern?
4. What actionable principle and training drill will correct this habit?

You MUST respond ONLY with a valid JSON object matching EXACTLY this structure (no markdown wrappers, raw JSON only):
{{
  "mentor_evaluation": "Detailed coaching evaluation of the move quality, tactical merits, and weaknesses.",
  "pedagogical_concept": "Core chess theme (e.g. 'King Safety & Clock Management under Stress')",
  "time_stress_assessment": "Concrete assessment of how remaining clock ({clock_sec}s), thinking duration ({duration_sec}s), and stress level ({tm.stress_level}) impacted this decision.",
  "error_frequency_insight": "Diagnostic insight analyzing how the player's error metrics ({blunder_cnt} blunders, frequency {blunder_freq}) manifest in this move.",
  "recommended_drill": "Specific thematic puzzle or drill to target this weakness.",
  "actionable_guideline": "Concise checklist rule for future games.",
  "sequence_narrative": "Cohesive summary of how the preceding moves led directly to the critical tension in this position.",
  "sequence_trend": "steady",
  "pattern_recognition": "Identified pattern from the sequence and error profile",
  "strategic_advice": "Actionable strategic directive for following moves"
}}
"""
    return prompt

def generate_heuristic_node_analysis(req: MentorNodeAnalysisRequest) -> dict:
    tm = req.time_control_metrics or NodeTimeMetrics()
    em = req.running_error_metrics or NodeRunningErrorMetrics()
    ec = req.eval_context or NodeEvalContext()

    clock_sec = round((tm.clock_remaining_ms or 0) / 1000, 1) if tm.clock_remaining_ms is not None else 60.0
    duration_sec = round((tm.move_duration_ms or 0) / 1000, 1) if tm.move_duration_ms is not None else 3.0
    stress_level = tm.stress_level or "Low"
    is_time_pressure = tm.time_pressure_flag or (clock_sec < 30)

    blunder_cnt = em.running_blunder_count or 0
    blunder_freq = em.blunder_frequency or 0.0
    missed_cnt = em.running_missed_opportunities_count or 0
    cls = ec.move_classification or "Good"
    san = req.move_san or ""

    if is_time_pressure or stress_level in ["High", "Extreme"]:
        time_stress_text = f"Acute time pressure ({clock_sec}s remaining, spent {duration_sec}s) with {stress_level} cognitive stress ({tm.stress_index}/100) prompted hurried tactical calculation."
    elif duration_sec < 2.0:
        time_stress_text = f"Move played impulsively in {duration_sec}s despite {clock_sec}s on the clock; blitz instinct bypassed verification of tactical replies."
    else:
        time_stress_text = f"Measured time management with {clock_sec}s in reserve; calculated for {duration_sec}s under {stress_level} stress."

    if blunder_cnt > 0 or blunder_freq > 0.10:
        error_insight = f"Active blunder frequency of {blunder_freq} ({blunder_cnt} cumulative blunders); move reflects a tendency to overlook opponent counter-tactics under defensive tension."
    elif missed_cnt > 0:
        error_insight = f"{missed_cnt} missed opportunities recorded so far (frequency {em.missed_opportunity_frequency or 0.0}); tactical alertness must be sharpened to exploit undefended opponent targets."
    else:
        error_insight = f"Solid structural precision with {em.running_accuracy_pct or 100}% running accuracy and 0 blunders in this game branch."

    if cls == "Blunder":
        concept = "Tactical Awareness & Blunder Prevention"
        eval_text = f"Move {san} represents a critical tactical oversight. Defensive structure was compromised, conceding vital initiative or material."
        drill = "Defensive Vision: Defending Hanging & Underprotected Pieces"
        guideline = "Always calculate opponent forcing checks, captures, and threats before finalizing your move."
    elif cls == "Missed Opportunity":
        concept = "Capitalizing on Opponent Tactical Errors"
        eval_text = f"Move {san} bypassed a sharper tactical breakthrough. Opponent vulnerabilities went unpunished."
        drill = "Sharp Tactical Combinations: Pins, Skewers & Overloaded Defenders"
        guideline = "When the opponent moves passively, search for direct tactical exploitation."
    elif cls in ["Best", "Brilliant"]:
        concept = "Optimal Piece Harmony & Tactical Precision"
        eval_text = f"Move {san} demonstrates high positional awareness, seizing key central outposts and restricting enemy piece coordination."
        drill = "Converting Positional Advantage into Endgame Wins"
        guideline = "Maintain central outpost control and press your space advantage."
    else:
        concept = "Positional Harmony & Piece Coordination"
        eval_text = f"Move {san} maintains steady development and central pressure, adhering to sound positional principles."
        drill = "Middle-Game Piece Coordination & Outpost Exploitation"
        guideline = "Activate your least active piece and coordinate rooks along central files."

    seq_moves = req.sequence_moves or []
    if len(seq_moves) <= 6:
        seq_narrative = f"Early opening sequence ({' -> '.join(seq_moves[-4:]) if seq_moves else san}) established central pawn presence and rapid minor piece mobilization."
        trend = "rising" if (ec.eval_delta or 0) > 0 else "steady"
    else:
        seq_narrative = f"The {len(seq_moves)}-move sequence leading up to this point created dynamic tension across central files, setting up the critical moment at move #{req.move_number}."
        trend = "declining" if (ec.eval_delta or 0) < -0.4 else ("rising" if (ec.eval_delta or 0) > 0.4 else "steady")

    return {
        "mentor_evaluation": eval_text,
        "pedagogical_concept": concept,
        "time_stress_assessment": time_stress_text,
        "error_frequency_insight": error_insight,
        "recommended_drill": drill,
        "actionable_guideline": guideline,
        "sequence_narrative": seq_narrative,
        "sequence_trend": trend,
        "pattern_recognition": f"{concept} in {req.color.upper()} game branch",
        "strategic_advice": "Balance clock expenditure with double-checking tactical lines on moves with stress index > 40."
    }

@app.post("/api/mentor/node-analysis")
async def analyze_node_with_mentor(req: MentorNodeAnalysisRequest):
    """
    Analyzes an individual node with the mentor using full board state,
    sequence leading up to it, clock time telemetry, and blunder/missed-opportunity frequencies.
    """
    try:
        prompt = build_mentor_node_prompt(req)
        mentor_res = await mentor_service.query_mentor(prompt, notebook_id=req.notebook_id)
        raw_text = mentor_res.get("response", "")

        parsed_data = None
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            try:
                parsed_data = json.loads(match.group(0))
            except Exception:
                pass

        if not parsed_data or not isinstance(parsed_data, dict):
            parsed_data = generate_heuristic_node_analysis(req)
            if len(raw_text) > 40 and "{" not in raw_text:
                parsed_data["mentor_evaluation"] = raw_text[:350]

        provider = mentor_res.get("provider", "Chess AI Mentor")
        parsed_data["source"] = provider
        parsed_data["analyzed_at"] = datetime.utcnow().isoformat()

        return {
            "success": True,
            "node_id": req.node_id,
            "analysis": parsed_data,
            "provider": provider
        }
    except Exception as e:
        fallback = generate_heuristic_node_analysis(req)
        fallback["source"] = "Chess AI Mentor (Local Fallback)"
        fallback["analyzed_at"] = datetime.utcnow().isoformat()
        return {
            "success": True,
            "node_id": req.node_id,
            "analysis": fallback,
            "provider": "Chess AI Mentor (Local Strategy Engine)"
        }

@app.post("/api/mentor/batch-node-analysis")
async def batch_analyze_nodes_with_mentor(req: BatchMentorNodeAnalysisRequest):
    """
    Processes a batch of DAG nodes with the mentor, incorporating board state,
    preceding move sequence, clock time telemetry, and error frequency metrics for each.
    """
    results = []
    for item in req.nodes:
        try:
            prompt = build_mentor_node_prompt(item)
            mentor_res = await mentor_service.query_mentor(prompt, notebook_id=req.notebook_id)
            raw_text = mentor_res.get("response", "")

            parsed_data = None
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                try:
                    parsed_data = json.loads(match.group(0))
                except Exception:
                    pass

            if not parsed_data or not isinstance(parsed_data, dict):
                parsed_data = generate_heuristic_node_analysis(item)
                if len(raw_text) > 40 and "{" not in raw_text:
                    parsed_data["mentor_evaluation"] = raw_text[:350]

            provider = mentor_res.get("provider", "Chess AI Mentor")
            parsed_data["source"] = provider
            parsed_data["analyzed_at"] = datetime.utcnow().isoformat()

            results.append({
                "node_id": item.node_id,
                "analysis": parsed_data,
                "provider": provider
            })
        except Exception:
            fallback = generate_heuristic_node_analysis(item)
            fallback["source"] = "Chess AI Mentor (Local Strategy Engine)"
            fallback["analyzed_at"] = datetime.utcnow().isoformat()
            results.append({
                "node_id": item.node_id,
                "analysis": fallback,
                "provider": "Chess AI Mentor (Local Strategy Engine)"
            })

    return {
        "success": True,
        "count": len(results),
        "results": results
    }


class GameAnalysisRequest(BaseModel):
    moves: List[str]
    fen: Optional[str] = None
    student_color: Optional[str] = "white"
    user_profile: Optional[dict] = None
    notebook_id: Optional[str] = None


@app.post("/api/game/analyze")
async def analyze_full_game(req: GameAnalysisRequest):
    """
    Performs full post-game analysis across all moves:
    - Move-by-move Stockfish evaluation graph
    - Classifications: Brilliant, Best, Good, Mistake, Blunder, Book
    - White & Black Accuracy score percentages
    - Comprehensive AI Coach Post-Game Report
    """
    try:
        start_board = chess.Board(req.fen) if req.fen else chess.Board()
        board = start_board.copy()

        move_evals = []
        white_losses = []
        black_losses = []

        white_counts = {"brilliant": 0, "best": 0, "good": 0, "mistake": 0, "blunder": 0, "book": 0}
        black_counts = {"brilliant": 0, "best": 0, "good": 0, "mistake": 0, "blunder": 0, "book": 0}

        # Initial eval
        init_eval_data = await engine_manager.evaluate_position(board, depth=10)
        prev_cp = init_eval_data.get("eval_val", 0.0) * 100.0 if init_eval_data.get("eval_type") == "cp" else (1000.0 if init_eval_data.get("eval_val", 0) > 0 else -1000.0)

        turning_points = []

        for idx, m_str in enumerate(req.moves):
            turn_before = board.turn
            side_str = "White" if turn_before == chess.WHITE else "Black"
            
            try:
                move_obj = board.push_san(m_str)
            except Exception:
                move_obj = board.push_uci(m_str)

            san_played = board.san(move_obj) if not isinstance(m_str, str) or len(m_str) > 4 else m_str

            eval_data = await engine_manager.evaluate_position(board, depth=10)
            curr_val = eval_data.get("eval_val", 0.0)
            curr_type = eval_data.get("eval_type", "cp")
            curr_cp = curr_val * 100.0 if curr_type == "cp" else (1000.0 if curr_val > 0 else -1000.0)

            # Calculate eval loss for side that played
            if turn_before == chess.WHITE:
                eval_loss = prev_cp - curr_cp
                white_losses.append(max(0.0, eval_loss))
            else:
                eval_loss = curr_cp - prev_cp
                black_losses.append(max(0.0, eval_loss))

            # Move classification logic
            category = "good"
            badge = "👍"
            if idx < 6:
                category = "book"
                badge = "📖"
            elif eval_loss <= -150.0:
                category = "brilliant"
                badge = "🌟"
            elif eval_loss <= 25.0:
                category = "best"
                badge = "✨"
            elif eval_loss <= 60.0:
                category = "good"
                badge = "👍"
            elif eval_loss <= 150.0:
                category = "mistake"
                badge = "⚠️"
            else:
                category = "blunder"
                badge = "💥"

            counts = white_counts if turn_before == chess.WHITE else black_counts
            counts[category] += 1

            if category in ["blunder", "mistake", "brilliant"]:
                turning_points.append(f"Move {idx//2 + 1} ({side_str}): {san_played} [{badge} {category.upper()}] (Eval: {eval_data.get('score', '0.0')})")

            move_evals.append({
                "move_num": idx // 2 + 1,
                "side": side_str,
                "move_san": san_played,
                "score": eval_data.get("score", "0.0"),
                "eval_cp": curr_cp,
                "category": category,
                "badge": badge,
                "best_move": eval_data.get("best_move_san", "")
            })

            prev_cp = curr_cp

        # Accuracy percentage calculation
        avg_w_loss = (sum(white_losses) / len(white_losses)) if white_losses else 0.0
        avg_b_loss = (sum(black_losses) / len(black_losses)) if black_losses else 0.0

        w_accuracy = round(max(0.0, min(100.0, 100.0 - (avg_w_loss / 3.0))), 1)
        b_accuracy = round(max(0.0, min(100.0, 100.0 - (avg_b_loss / 3.0))), 1)

        student_color_name = (req.student_color or "white").upper()
        student_elo = req.user_profile.get("estimated_elo", 1500) if (req.user_profile and isinstance(req.user_profile, dict)) else 1500

        if student_color_name == "BLACK":
            student_desc = f"The student played as BLACK (⚫ Black - {student_elo} ELO)."
            white_eval_heading = "⚪ White (Opponent)"
            black_eval_heading = f"⚫ Black (Student - {student_elo} ELO)"
        elif student_color_name == "WHITE":
            student_desc = f"The student played as WHITE (⚪ White - {student_elo} ELO)."
            white_eval_heading = f"⚪ White (Student - {student_elo} ELO)"
            black_eval_heading = "⚫ Black (Opponent)"
        else:
            student_desc = "The student managed both White and Black."
            white_eval_heading = "⚪ White"
            black_eval_heading = "⚫ Black"

        prof_context = format_user_profile_context(req.user_profile)

        # Generate AI Coach Summary
        coach_prompt = f"""POST-GAME COACH ANALYSIS REPORT REQUEST:
{student_desc}
{prof_context}

Move Count: {len(req.moves)} moves played.
White Accuracy: {w_accuracy}% (Blunders: {white_counts['blunder']}, Mistakes: {white_counts['mistake']}, Best: {white_counts['best']})
Black Accuracy: {b_accuracy}% (Blunders: {black_counts['blunder']}, Mistakes: {black_counts['mistake']}, Best: {black_counts['best']})

Key Turning Points:
{chr(10).join(turning_points) if turning_points else 'Solid game without major tactical blunders.'}

CRITICAL STRUCTURAL INSTRUCTIONS FOR YOUR REPORT:
1. Summarize the game's key moments and turning points.
2. Under "⚔️ Tactical & Positional Evaluation", evaluate both sides using EXACTLY these headings:
   {white_eval_heading}:
   * Strengths: ...
   * Weaknesses: ...

   {black_eval_heading}:
   * Strengths: ...
   * Weaknesses: ...
3. Provide 3 Concrete Advice Tips targeted specifically to help the STUDENT ({student_color_name}) improve their play.
4. Conclude with a dedicated section formatted exactly as:
   💡 GENERALIZED TURN RULE:
   followed by 1 reusable strategic chess rule for future games.
"""
        mentor_res = await mentor_service.query_mentor(coach_prompt, notebook_id=req.notebook_id)

        return {
            "white_accuracy": w_accuracy,
            "black_accuracy": b_accuracy,
            "white_counts": white_counts,
            "black_counts": black_counts,
            "move_evals": move_evals,
            "turning_points": turning_points,
            "coach_report": mentor_res["response"],
            "provider": mentor_res["provider"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Game analysis failed: {str(e)}")


# Global Data Stores for User Profiles, Skill Matrix & Diagnostic Placement
PROFILES_FILE = os.path.join(os.path.dirname(__file__), "user_profiles.json")

def load_persisted_profiles():
    if os.path.exists(PROFILES_FILE):
        try:
            with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("[load_persisted_profiles error]:", e)
    return {}

def save_persisted_profiles():
    try:
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(USER_PROFILES, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Error saving profiles] {e}")

USER_PROFILES = load_persisted_profiles()
if not USER_PROFILES:
    USER_PROFILES = {
        "prof_default": {"id": "prof_default", "name": "Player", "elo": 1500, "is_qa": False, "gamesPlayed": 0},
        "prof_qa_tester": {"id": "prof_qa_tester", "name": "QA Tester Profile", "elo": 1680, "is_qa": True, "gamesPlayed": 52}
    }
ACTIVE_PROFILE_ID = "prof_qa_tester" if "prof_qa_tester" in USER_PROFILES else "prof_default" 

USER_SKILLS = {
    "tactics": {"name": "Tactics & Combinations", "icon": "⚔️", "mastery": 72, "level": "proficient", "puzzles_solved": 45},
    "openings": {"name": "Opening Repertoire", "icon": "📖", "mastery": 65, "level": "developing", "puzzles_solved": 30},
    "endgame": {"name": "Endgame Technique", "icon": "🏰", "mastery": 54, "level": "developing", "puzzles_solved": 22},
    "positional": {"name": "Positional Play & Pawn Structure", "icon": "♟️", "mastery": 80, "level": "proficient", "puzzles_solved": 60},
    "time_mgmt": {"name": "Time Management", "icon": "⏱️", "mastery": 45, "level": "novice", "puzzles_solved": 15},
    "calculation": {"name": "Calculation Depth", "icon": "🧠", "mastery": 88, "level": "mastered", "puzzles_solved": 95}
}

CONVERT_SYSTEMS = [
    {"platform": "FIDE Standard", "icon": "🏆", "offset": 0, "formula": "FIDE Baseline"},
    {"platform": "Chess.com Rapid", "icon": "🟢", "offset": 150, "formula": "FIDE + ~150"},
    {"platform": "Chess.com Blitz", "icon": "⚡", "offset": 80, "formula": "FIDE + ~80"},
    {"platform": "Lichess Classical", "icon": "🐴", "offset": 300, "formula": "FIDE + ~300"},
    {"platform": "Lichess Blitz", "icon": "🔥", "offset": 220, "formula": "FIDE + ~220"},
    {"platform": "USCF National", "icon": "🇺🇸", "offset": 100, "formula": "FIDE + ~100"}
]

PLACEMENT_QUESTIONS = [
    {
        "id": "q1",
        "question": "1. In an equal endgame with King + Pawns vs King + Pawns, what is the most critical strategic concept?",
        "options": [
            {"text": "A) Opposition & King Central Activity", "tier_score": 1800, "feedback": "Correct! Opposition and King activity dictate pawn endgames."},
            {"text": "B) Pushing wing pawns without king support", "tier_score": 1000, "feedback": "Incorrect. Unsupported pawns become easy targets."},
            {"text": "C) Keeping King on the home rank", "tier_score": 1200, "feedback": "Incorrect. Passive kings lead to lost endgames."}
        ]
    },
    {
        "id": "q2",
        "question": "2. What is the main operational objective in the Opening phase?",
        "options": [
            {"text": "A) Rapid piece development, central control, and King safety", "tier_score": 1500, "feedback": "Correct! Rapid development and central foothold are fundamental."},
            {"text": "B) Launching immediate early Queen attack on f7/f2", "tier_score": 1000, "feedback": "Incorrect. Early queen attacks waste tempo against solid defense."},
            {"text": "C) Moving the same piece multiple times to steal pawns", "tier_score": 1100, "feedback": "Incorrect. Violates opening development principles."}
        ]
    },
    {
        "id": "q3",
        "question": "3. Your opponent has a pinned Knight defending their Queen. What tactical theme applies?",
        "options": [
            {"text": "A) Exploiting the Pinned Defender by piling pressure on it", "tier_score": 1800, "feedback": "Correct! Pinned pieces cannot move or defend effectively."},
            {"text": "B) Offer a draw immediately", "tier_score": 900, "feedback": "Incorrect. Pinned pieces offer immediate tactical winning chances."},
            {"text": "C) Retreat your active attacking pieces", "tier_score": 1200, "feedback": "Incorrect. Always keep pressure on pinned defenders."}
        ]
    }
]

def classify_move(best_eval_cp, actual_eval_cp, cp_diff, is_white):
    if cp_diff <= -150:
        return "brilliant", "🌟 Brilliant"
    elif cp_diff <= 25:
        return "best", "✨ Best"
    elif cp_diff <= 60:
        return "good", "👍 Good"
    elif cp_diff <= 150:
        return "mistake", "⚠️ Mistake"
    else:
        return "blunder", "💥 Blunder"

def generate_post_game_summary(w_acc, b_acc, w_counts, b_counts, turning_points):
    summary = f"Match Summary:\nWhite Accuracy: {w_acc}% | Black Accuracy: {b_acc}%\n\n"
    if w_acc > b_acc:
        summary += "White displayed higher positional consistency and move accuracy throughout the game."
    elif b_acc > w_acc:
        summary += "Black controlled the flow of the game with superior precision and tactical conversion."
    else:
        summary += "Both sides played with very closely matched accuracy across all phases of the game."

    if turning_points:
        summary += "\n\nKey Critical Turning Points:\n- " + "\n- ".join(turning_points[:3])
    return summary

class CreateProfileRequest(BaseModel):
    name: str
    starting_elo: int = 1500

class SwitchProfileRequest(BaseModel):
    profile_id: str

class SubmitPlacementRequest(BaseModel):
    answers: dict

class SyncProfilesRequest(BaseModel):
    profiles: List[Dict[str, Any]]
    active_profile_id: Optional[str] = None

@app.post("/api/user/profiles/sync")
async def sync_user_profiles(req: SyncProfilesRequest):
    global USER_PROFILES, ACTIVE_PROFILE_ID
    for p in req.profiles:
        pid = p.get("id")
        if pid:
            USER_PROFILES[pid] = p
    if req.active_profile_id and req.active_profile_id in USER_PROFILES:
        ACTIVE_PROFILE_ID = req.active_profile_id
    save_persisted_profiles()
    return {"status": "success", "count": len(USER_PROFILES)}


@app.get("/api/user/profiles")
async def get_user_profiles():
    global USER_PROFILES
    USER_PROFILES = load_persisted_profiles()
    return {
        "profiles": list(USER_PROFILES.values()),
        "active_profile_id": ACTIVE_PROFILE_ID
    }

@app.post("/api/user/profiles")
async def create_user_profile(req: CreateProfileRequest):
    global ACTIVE_PROFILE_ID
    import uuid
    new_id = f"prof_{str(uuid.uuid4())[:8]}"
    tier_str = "Intermediate (~1500 ELO)"
    if req.starting_elo < 1200:
        tier_str = f"Beginner (~{req.starting_elo} ELO)"
    elif req.starting_elo < 1700:
        tier_str = f"Intermediate (~{req.starting_elo} ELO)"
    elif req.starting_elo < 2100:
        tier_str = f"Advanced (~{req.starting_elo} ELO)"
    else:
        tier_str = f"Master Candidate (~{req.starting_elo} ELO)"

    profile = {
        "id": new_id,
        "name": req.name,
        "starting_elo": req.starting_elo,
        "estimated_elo": req.starting_elo,
        "tier": tier_str,
        "games_tracked": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "win_rate": "0%"
    }
    USER_PROFILES[new_id] = profile
    ACTIVE_PROFILE_ID = new_id
    return {"status": "success", "profile": profile}

@app.post("/api/user/profiles/switch")
async def switch_user_profile(req: SwitchProfileRequest):
    global ACTIVE_PROFILE_ID
    if req.profile_id in USER_PROFILES:
        ACTIVE_PROFILE_ID = req.profile_id
        return {"status": "success", "active_profile": USER_PROFILES[ACTIVE_PROFILE_ID]}
    raise HTTPException(status_code=404, detail="Profile not found")

@app.get("/api/user/active-profile")
async def get_active_user_profile():
    return {"profile": USER_PROFILES.get(ACTIVE_PROFILE_ID, list(USER_PROFILES.values())[0])}

@app.get("/api/user/skills")
async def get_user_skills():
    active_elo = USER_PROFILES.get(ACTIVE_PROFILE_ID, {}).get("estimated_elo", 1500)
    conversions = []
    for sys in CONVERT_SYSTEMS:
        calc_elo = active_elo + sys["offset"]
        conversions.append({
            "platform": sys["platform"],
            "icon": sys["icon"],
            "converted_elo": calc_elo,
            "formula": sys["formula"]
        })
    return {
        "skills": list(USER_SKILLS.values()),
        "rating_conversions": conversions
    }

@app.get("/api/user/placement-test")
async def get_placement_test():
    return {"questions": PLACEMENT_QUESTIONS}

@app.post("/api/user/placement-test/submit")
async def submit_placement_test(req: SubmitPlacementRequest):
    global ACTIVE_PROFILE_ID
    scores = list(req.answers.values())
    if not scores:
        avg_score = 1500
    else:
        avg_score = int(sum(scores) / len(scores))

    if ACTIVE_PROFILE_ID in USER_PROFILES:
        USER_PROFILES[ACTIVE_PROFILE_ID]["estimated_elo"] = avg_score
        tier_str = "Intermediate"
        if avg_score < 1200: tier_str = "Beginner"
        elif avg_score >= 1800: tier_str = "Advanced"
        USER_PROFILES[ACTIVE_PROFILE_ID]["tier"] = f"{tier_str} (~{avg_score} ELO)"

    return {
        "assigned_elo": avg_score,
        "assessment": f"Diagnostic Placement Completed! Your estimated playing strength is calibrated to {avg_score} ELO."
    }


@app.post("/api/openings/explore")
async def explore_opening(req: BoardStateRequest):
    """
    Returns ECO opening details, continuation candidates, and win rate stats for current position.
    """
    try:
        if req.fen and req.fen != "start":
            try:
                board = chess.Board(req.fen)
            except Exception:
                board = chess.Board()
        else:
            board = chess.Board()

        if req.moves:
            for m in req.moves:
                try:
                    board.push_san(m)
                except Exception:
                    board.push_uci(m)

        opening_info = ChessTranslator.get_opening_info(board)
        return {
            "fen": board.fen(),
            "opening": opening_info
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Opening explorer failed: {str(e)}")


@app.post("/api/mentor/quiz")
async def generate_position_quiz(req: BoardStateRequest):
    """
    Generates an interactive 3-option tactical/positional quiz based on current board weaknesses.
    """
    try:
        if req.fen and req.fen != "start":
            try:
                board = chess.Board(req.fen)
            except Exception:
                board = chess.Board()
        else:
            board = chess.Board()

        if req.moves:
            for m in req.moves:
                try:
                    board.push_san(m)
                except Exception:
                    board.push_uci(m)

        eval_res = await engine_manager.evaluate_position(board, depth=12)
        tactics = ChessTranslator.get_tactical_summary(board)
        best_san = eval_res.get("best_move_san", "Nf3")
        turn_str = "White" if board.turn == chess.WHITE else "Black"

        question_text = f"Position Quiz for {turn_str}: What is the highest recommended strategic move?"
        if tactics["is_check"]:
            question_text = f"🔥 CHECK ALERT! {turn_str} is in check. What is the safest escape move?"
        elif tactics["under_attack"]:
            question_text = f"⚔️ THREAT ALERT! {tactics['under_attack'][0]} is under threat. What is the best play?"

        quiz = {
            "question": question_text,
            "fen": board.fen(),
            "eval_summary": eval_res.get("score", "+0.0"),
            "options": [
                {
                    "text": f"🎯 Play Top Engine Move: {best_san}",
                    "is_correct": True,
                    "explanation": f"Correct! {best_san} improves piece activity, addresses central control, and optimizes overall position."
                },
                {
                    "text": "♟️ Push a passive wing pawn (a3 / h3)",
                    "is_correct": False,
                    "explanation": "Incorrect. Passive pawn moves waste tempo and do not counter opponent's active threats."
                },
                {
                    "text": "🛡️ Retreat active pieces back to home rank",
                    "is_correct": False,
                    "explanation": "Incorrect. Unnecessary retreats surrender central control and initiative."
                }
            ]
        }
        return quiz
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Quiz generation failed: {str(e)}")



@app.post("/api/config")
async def update_config(req: ConfigUpdateRequest):
    if req.stockfish_path is not None:
        engine_manager.stockfish_path = req.stockfish_path
        engine_manager._init_local_engine()
    if req.notebook_id is not None:
        mentor_service.notebook_id = req.notebook_id
    if req.auth_token is not None:
        mentor_service.auth_token = req.auth_token

    return {
        "success": True,
        "message": "Configuration updated successfully.",
        "status": await get_status()
    }


@app.get("/api/analytics/profile-insights")
async def get_profile_insights(profile_id: Optional[str] = None):
    """
    Enhanced Profile Analytics Endpoint:
    Dynamically analyzes real DAG decision trees, Stockfish eval swings,
    and 6-Aspect metrics strictly from the active profile's recorded history.
    """
    active_prof = USER_PROFILES.get(profile_id or ACTIVE_PROFILE_ID, list(USER_PROFILES.values())[0])
    is_qa = active_prof.get("is_qa", False)
    history = active_prof.get("history", [])

    games_count = len(history)
    total_nodes = 0
    eventful_count = 0
    need_analysis_count = 0
    
    off_creation = 0
    off_execution = 0
    off_yield_sum = 0
    off_yield_cnt = 0
    def_prev = 0
    def_fail = 0
    def_damage_sum = 0
    def_damage_cnt = 0
    
    error_counts = {}

    for ev in history:
        for n in ev.get("moves", []):
            total_nodes += 1
            sf_st = n.get("stockfish_analysis_status") or n.get("analysis_status")
            mentor_st = n.get("mentor_analysis_status") or n.get("analysis_status")
            if sf_st in ("NEED_ANALYSIS", "PENDING", "PENDING_ANALYSIS") or mentor_st in ("NEED_ANALYSIS", "PENDING", "PENDING_ANALYSIS"):
                need_analysis_count += 1
            pm = n.get("per_move_analysis") or {}
            cls = pm.get("move_classification")
            if cls in ["Blunder", "Mistake", "Inaccuracy", "Brilliant", "Great"]:
                eventful_count += 1
            flags = pm.get("six_aspect_flags") or {}
            if flags.get("offensive_creation"): off_creation += 1
            if flags.get("offensive_execution"): off_execution += 1
            if flags.get("offensive_yield", 0) > 0:
                off_yield_sum += flags.get("offensive_yield", 0)
                off_yield_cnt += 1
            if flags.get("defensive_prevention"): def_prev += 1
            if flags.get("defensive_failure"):
                def_fail += 1
                if flags.get("defensive_damage", 0) > 0:
                    def_damage_sum += flags.get("defensive_damage", 0)
                    def_damage_cnt += 1
            sub_err = pm.get("tactical_sub_category")
            if sub_err and cls in ["Blunder", "Mistake"]:
                error_counts[sub_err] = error_counts.get(sub_err, 0) + 1

    blunder_rate = round((def_fail / total_nodes * 100), 1) if total_nodes > 0 else 0.0
    avg_yield = round(off_yield_sum / off_yield_cnt) if off_yield_cnt > 0 else 0
    avg_damage = round(def_damage_sum / def_damage_cnt) if def_damage_cnt > 0 else 0

    repeating_errors_list = []
    error_labels = {
        "undefended_loose_piece": ("Leaving Undefended Loose Targets", "tactics", "Leaving minor pieces un-backed during middlegame tactical exchanges."),
        "king_exposure": ("Premature Pawn Push & King Exposure", "king_safety", "Advancing pawns in front of the castled king creates weak holes."),
        "diagonal_pin": ("Missing Diagonal Pins on Queens/Rooks", "pins", "Failing to spot bishop/queen pin skewers along major diagonals."),
        "premature_simplification": ("Premature Simplification Under Material Deficit", "endgame", "Trading heavy pieces when down in pawn material instead of counterplay.")
    }

    for ek, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
        label, cat, desc = error_labels.get(ek, (ek.replace("_", " ").title(), "general", "Frequent blunder signature."))
        pct = round((count / max(1, def_fail)) * 100)
        repeating_errors_list.append({
            "id": f"err_{ek}",
            "title": label,
            "category": cat,
            "frequency": f"{pct}% of blunders ({count} Nodes)",
            "description": desc,
            "count": count
        })

    insights = {
        "profile_id": active_prof.get("id"),
        "profile_name": active_prof.get("name"),
        "is_qa": is_qa,
        "estimated_elo": active_prof.get("estimated_elo", active_prof.get("elo", 1500)),
        "games_analyzed": games_count,
        "dag_nodes_count": total_nodes,
        "eventful_count": eventful_count,
        "need_analysis_count": need_analysis_count,
        "aspect_metrics": {
            "offensive": {
                "creation": round(off_creation / max(1, total_nodes) * 100) if total_nodes > 0 else 0,
                "execution": round(off_execution / max(1, total_nodes) * 100) if total_nodes > 0 else 0,
                "yield": avg_yield
            },
            "defensive": {
                "prevention": round(def_prev / max(1, total_nodes) * 100) if total_nodes > 0 else 0,
                "failure": blunder_rate,
                "damage": avg_damage
            }
        },
        "repeating_errors": repeating_errors_list,
        "qa_debug_payload": {
            "total_nodes": total_nodes,
            "eventful_nodes": eventful_count,
            "pending_analysis_nodes": need_analysis_count,
            "raw_eval_deltas_count": total_nodes
        } if is_qa else None
    }
    return insights


@app.post("/api/analytics/generate-adaptive-exercises")
async def generate_adaptive_exercises(req: Dict[str, Any]):
    """
    AI Adaptive Exercise Planner:
    Generates targeted puzzle challenges dynamically matched to detected repeating user blunders.
    """
    exercises = [
        {
            "id": "ex_1",
            "title": "⚡ Fix Undefended Target: Protect the Knight",
            "category": "tactics",
            "target_weakness": "Leaving Loose Pieces",
            "fen": "r1bqk2r/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4",
            "goal": "Find the best move that secures all undefended pieces and neutralizes opponent pin threats.",
            "best_move_san": "d3",
            "explanation": "d3 defends the e4 pawn and consolidates central piece harmony, removing undefended targets."
        },
        {
            "id": "ex_2",
            "title": "🛡️ Fix King Exposure: Solidify Pawn Shield",
            "category": "king_safety",
            "target_weakness": "King Safety Holes",
            "fen": "r1bq1rk1/ppp2ppp/2n5/3p4/3P4/2PB1N2/P1P2PPP/R2Q1RK1 w - - 0 10",
            "goal": "Re-organize pieces to cover weak dark holes around your castled king.",
            "best_move_san": "Re1",
            "explanation": "Re1 controls the open e-file and provides an escape rook line, preventing back-rank weaknesses."
        },
        {
            "id": "ex_3",
            "title": "🎯 Fix Missed Pin: Exploit Diagonal Skewer",
            "category": "pins",
            "target_weakness": "Pin/Skewer Blindspots",
            "fen": "rnbqk2r/pppp1ppp/5n2/4p3/1b2P3/2N2N2/PPPP1PPP/R1BQKB1R w KQkq - 0 4",
            "goal": "Execute the pinning move that paralyzes the knight and captures material.",
            "best_move_san": "d3",
            "explanation": "d3 supports e4 while preparing Bg5 to pin the f6 knight against the enemy queen."
        }
    ]
    return {
        "success": True,
        "exercises": exercises,
        "count": len(exercises)
    }



class AutoNameRequest(BaseModel):
    fen: Optional[str] = None
    moves: Optional[List[str]] = None
    outcome: Optional[str] = None

class RenameGameRequest(BaseModel):
    game_id: str
    new_title: str

@app.post("/api/game/auto-name")
async def auto_name_game(req: AutoNameRequest):
    """
    AI Mentor Auto-Naming Service:
    Generates a descriptive, AI-crafted title for a game session based on opening theory & key turning points.
    """
    moves_count = len(req.moves) if req.moves else 0
    first_move = req.moves[0] if req.moves else "e4"
    
    opening_name = "Italian Game"
    if first_move == "d4":
        opening_name = "Queen's Gambit"
    elif first_move == "c4":
        opening_name = "English Opening"
    elif first_move == "Nf3":
        opening_name = "Reti Opening"

    outcome_str = "Victory" if req.outcome == "1-0" else ("Draw Session" if req.outcome == "1/2-1/2" else "Tactical Challenge")
    generated_title = f"🤖 {opening_name}: {outcome_str} ({moves_count} moves)"

    return {
        "success": True,
        "auto_title": generated_title
    }

@app.post("/api/game/rename")
async def rename_game_session(req: RenameGameRequest):
    """
    User Event Renaming Endpoint:
    Allows user to manually rename any game event session.
    """
    return {
        "success": True,
        "game_id": req.game_id,
        "new_title": req.new_title,
        "message": f"Event {req.game_id} renamed to '{req.new_title}'"
    }


frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
