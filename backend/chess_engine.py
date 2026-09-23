import os
import chess
import chess.engine
import httpx
from typing import Dict, Any, List, Optional
from backend.config import STOCKFISH_PATH

class ChessEngineManager:
    """
    Manages chess board state and Stockfish evaluation (local executable or cloud fallback).
    """

    def __init__(self, stockfish_path: str = ""):
        self.stockfish_path = stockfish_path or STOCKFISH_PATH
        self._engine: Optional[chess.engine.SimpleEngine] = None
        self._init_local_engine()

    def _init_local_engine(self):
        candidates = []
        if self.stockfish_path and os.path.exists(self.stockfish_path):
            candidates.append(self.stockfish_path)
        
        # Check standard default locations on Windows/Linux
        candidates.extend([
            "stockfish.exe",
            "stockfish/stockfish.exe",
            "C:\\stockfish\\stockfish.exe",
            "/usr/games/stockfish",
            "/usr/local/bin/stockfish"
        ])

        for path in candidates:
            if os.path.exists(path) or (os.name == 'posix' and os.access(path, os.X_OK)):
                try:
                    self._engine = chess.engine.SimpleEngine.popen_uci(path)
                    print(f"[EngineManager] Connected to local Stockfish at: {path}")
                    return
                except Exception as e:
                    print(f"[EngineManager] Could not start Stockfish at {path}: {e}")
        
        print("[EngineManager] Local Stockfish binary not found. Will use Cloud/Heuristic evaluation.")

    def close(self):
        if self._engine:
            try:
                self._engine.quit()
            except Exception:
                pass

    async def evaluate_position(self, board: chess.Board, depth: int = 14) -> Dict[str, Any]:
        """
        Calculates evaluation (centipawns or mate), top 3 candidate moves, and recommended line.
        """
        # 1. Try Local Stockfish
        if self._engine:
            try:
                info = self._engine.analyse(board, chess.engine.Limit(depth=depth), multipv=3)
                best_line = info[0] if isinstance(info, list) else info
                score_obj = best_line["score"].relative

                if score_obj.is_mate():
                    mate_val = score_obj.mate()
                    eval_type = "mate"
                    eval_val = mate_val
                    formatted_score = f"M{abs(mate_val)}" if mate_val > 0 else f"-M{abs(mate_val)}"
                else:
                    cp_val = score_obj.score()
                    eval_type = "cp"
                    eval_val = round(cp_val / 100.0, 2)
                    formatted_score = f"{'+' if eval_val > 0 else ''}{eval_val}"

                top_moves = []
                lines_list = info if isinstance(info, list) else [info]
                for item in lines_list:
                    pv = item.get("pv", [])
                    if pv:
                        move = pv[0]
                        move_san = board.san(move)
                        top_moves.append({
                            "uci": move.uci(),
                            "san": move_san,
                            "score": str(item.get("score", "").relative) if "score" in item else ""
                        })

                best_move = top_moves[0]["uci"] if top_moves else ""
                best_move_san = top_moves[0]["san"] if top_moves else ""

                return {
                    "source": "local_stockfish",
                    "score": formatted_score,
                    "eval_type": eval_type,
                    "eval_val": eval_val,
                    "best_move": best_move,
                    "best_move_san": best_move_san,
                    "top_moves": top_moves,
                    "depth": depth
                }
            except Exception as e:
                print(f"[EngineManager] Local engine analysis failed: {e}")

        # 2. Try Lichess Cloud API
        cloud_eval = await self._fetch_cloud_eval(board.fen())
        if cloud_eval:
            return cloud_eval

        # 3. Heuristic Fallback based on material balance & active board state
        return self._heuristic_eval(board)

    async def _fetch_cloud_eval(self, fen: str) -> Optional[Dict[str, Any]]:
        try:
            url = f"https://lichess.org/api/cloud-eval?fen={httpx.QueryParams({'fen': fen})['fen']}"
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    pvs = data.get("pvs", [])
                    if pvs:
                        first_pv = pvs[0]
                        cp = first_pv.get("cp")
                        mate = first_pv.get("mate")
                        moves = first_pv.get("moves", "").split()

                        if mate is not None:
                            formatted_score = f"M{abs(mate)}" if mate > 0 else f"-M{abs(mate)}"
                            eval_val = mate
                            eval_type = "mate"
                        else:
                            eval_val = round((cp or 0) / 100.0, 2)
                            formatted_score = f"{'+' if eval_val > 0 else ''}{eval_val}"
                            eval_type = "cp"

                        best_uci = moves[0] if moves else ""
                        top_moves_list = []
                        for m_uci in moves[:3]:
                            try:
                                m_obj = chess.Move.from_uci(m_uci)
                                m_san = board.san(m_obj)
                            except Exception:
                                m_san = m_uci
                            top_moves_list.append({"uci": m_uci, "san": m_san})

                        best_san = top_moves_list[0]["san"] if top_moves_list else best_uci

                        return {
                            "source": "lichess_cloud",
                            "score": formatted_score,
                            "eval_type": eval_type,
                            "eval_val": eval_val,
                            "best_move": best_uci,
                            "best_move_san": best_san,
                            "top_moves": top_moves_list,
                            "depth": data.get("depth", 12)
                        }
        except Exception as e:
            print(f"[EngineManager] Cloud evaluation fetch failed: {e}")
        return None

    def _heuristic_eval(self, board: chess.Board) -> Dict[str, Any]:
        """
        Fast heuristic evaluation based on material values & piece position.
        """
        PIECE_VALUES = {
            chess.PAWN: 1.0,
            chess.KNIGHT: 3.0,
            chess.BISHOP: 3.25,
            chess.ROOK: 5.0,
            chess.QUEEN: 9.0,
            chess.KING: 0.0
        }
        score = 0.0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                val = PIECE_VALUES.get(piece.piece_type, 0.0)
                score += val if piece.color == chess.WHITE else -val

        turn_mult = 1.0 if board.turn == chess.WHITE else -1.0
        rel_score = round(score * turn_mult, 2)
        formatted_score = f"{'+' if rel_score > 0 else ''}{rel_score}"

        legal_moves = list(board.legal_moves)
        best_uci = legal_moves[0].uci() if legal_moves else ""
        best_san = board.san(legal_moves[0]) if legal_moves else ""

        return {
            "source": "heuristic",
            "score": formatted_score,
            "eval_type": "cp",
            "eval_val": rel_score,
            "best_move": best_uci,
            "best_move_san": best_san,
            "top_moves": [{"uci": m.uci(), "san": board.san(m)} for m in legal_moves[:3]],
            "depth": 1
        }
