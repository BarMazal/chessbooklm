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


class MentorExplainRequest(BaseModel):
    fen: str
    moves: Optional[List[str]] = None
    mode: Optional[str] = "human"  # "human" or "raw_fen"
    question: Optional[str] = None
    notebook_id: Optional[str] = None


class ConfigUpdateRequest(BaseModel):
    stockfish_path: Optional[str] = None
    notebook_id: Optional[str] = None
    auth_token: Optional[str] = None


class SelectNotebookRequest(BaseModel):
    notebook_id: str


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
async def trigger_login():
    """
    Triggers notebooklm login process in browser.
    """
    return await mentor_service.trigger_login()


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
    Returns list of all available NotebookLM notebooks for the user.
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


@app.post("/api/board/evaluate")
async def evaluate_board(req: BoardStateRequest):
    try:
        if req.moves and len(req.moves) > 0:
            board = chess.Board()
            for m in req.moves:
                try:
                    board.push_san(m)
                except Exception:
                    try:
                        board.push_uci(m)
                    except Exception:
                        pass
        elif req.fen:
            board = chess.Board(req.fen)
        else:
            board = chess.Board()

        eval_res = await engine_manager.evaluate_position(board, depth=req.depth or 12)
        opening_name = ChessTranslator.identify_opening(board)
        tactics = ChessTranslator.get_tactical_summary(board)

        legal_moves = [{"uci": m.uci(), "san": board.san(m)} for m in board.legal_moves]

        return {
            "fen": board.fen(),
            "turn": "white" if board.turn == chess.WHITE else "black",
            "opening": opening_name,
            "is_check": board.is_check(),
            "is_game_over": board.is_game_over(),
            "eval": eval_res,
            "tactics": tactics,
            "legal_moves": legal_moves
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid board evaluation request: {str(e)}")


@app.post("/api/mentor/explain")
async def explain_position(req: MentorExplainRequest):
    try:
        if req.moves and len(req.moves) > 0:
            board = chess.Board()
            for m in req.moves:
                try:
                    board.push_san(m)
                except Exception:
                    try:
                        board.push_uci(m)
                    except Exception:
                        pass
        elif req.fen:
            board = chess.Board(req.fen)
        else:
            board = chess.Board()

        eval_res = await engine_manager.evaluate_position(board, depth=12)

        if req.mode == "raw_fen":
            prompt = ChessTranslator.translate_raw_fen_mode(req.fen, req.question)
        else:
            prompt = ChessTranslator.translate_position_to_human(board, eval_res, req.question)

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
