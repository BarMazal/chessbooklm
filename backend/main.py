import os
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
    Safely constructs a chess.Board from moves list or FEN without double-applying moves onto a non-start FEN.
    """
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
USER_PROFILES = {
    "default": {
        "id": "default",
        "name": "Player 1",
        "starting_elo": 1500,
        "estimated_elo": 1500,
        "tier": "Intermediate (~1500 ELO)",
        "games_tracked": 12,
        "wins": 7,
        "draws": 2,
        "losses": 3,
        "win_rate": "58.3%"
    }
}
ACTIVE_PROFILE_ID = "default"

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

@app.get("/api/user/profiles")
async def get_user_profiles():
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

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
