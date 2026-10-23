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
        self._resolved_engine_path: Optional[str] = None
        self._engine: Optional[chess.engine.SimpleEngine] = None
        self._review_cache: Dict[Any, Dict[str, Any]] = {}
        self._init_local_engine()

    def _init_local_engine(self):
        candidates = []
        if self.stockfish_path and os.path.exists(self.stockfish_path):
            candidates.append(self.stockfish_path)
        
        # Check standard default locations on Windows/Linux/macOS
        candidates.extend([
            "stockfish.exe",
            "stockfish/stockfish.exe",
            "stockfish/stockfish",
            "stockfish/stockfish-windows-x86-64-universal.exe",
            "stockfish/stockfish-ubuntu-x86-64-universal",
            "stockfish/stockfish-macos-x86-64-universal",
            "C:\\stockfish\\stockfish.exe",
            "/usr/games/stockfish",
            "/usr/local/bin/stockfish"
        ])

        # Relative candidates resolve against the project root, not the launch directory
        # (Windows cannot spawn a relative "stockfish/stockfish.exe" reliably).
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidates = [p if os.path.isabs(p) else os.path.join(project_root, p) for p in candidates]

        for path in candidates:
            if os.path.exists(path) or (os.name == 'posix' and os.access(path, os.X_OK)):
                try:
                    self._engine = chess.engine.SimpleEngine.popen_uci(path)
                    self._resolved_engine_path = path
                    # The engine's I/O thread is non-daemon; quit it before the interpreter waits on it.
                    try:
                        import threading
                        threading._register_atexit(self.close)
                    except Exception:
                        pass
                    print(f"[EngineManager] Connected to local Stockfish at: {path}")
                    return
                except Exception as e:
                    print(f"[EngineManager] Could not start Stockfish at {path}: {e}")
        
        print("[EngineManager] Local Stockfish binary not found. Will use Cloud/Heuristic evaluation.")

    def _ensure_engine(self) -> Optional[chess.engine.SimpleEngine]:
        """Ensures the local Stockfish engine is alive; restarts it if it terminated."""
        if self._engine:
            try:
                # Check if underlying subprocess is still alive
                proc = self._engine.transport.get_extra_info("subprocess")
                if proc and proc.poll() is not None:
                    # Process died
                    self._engine = None
            except Exception:
                self._engine = None

        if self._engine is None and self._resolved_engine_path and os.path.exists(self._resolved_engine_path):
            try:
                self._engine = chess.engine.SimpleEngine.popen_uci(self._resolved_engine_path)
                print(f"[EngineManager] Successfully reconnected to local Stockfish at: {self._resolved_engine_path}")
            except Exception as e:
                print(f"[EngineManager] Failed to restart local Stockfish: {e}")
                self._engine = None

        return self._engine

    def close(self):
        if self._engine:
            try:
                self._engine.quit()
            except Exception:
                pass
            self._engine = None

    async def evaluate_position(self, board: chess.Board, depth: int = 14) -> Dict[str, Any]:
        """
        Calculates evaluation (centipawns or mate), top 3 candidate moves, and recommended line.
        """
        # 1. Try Local Stockfish (only if board is legally valid; UCI engines crash on illegal positions)
        engine = self._ensure_engine()
        if engine and board.is_valid():
            try:
                info = engine.analyse(board, chess.engine.Limit(depth=depth), multipv=3)
                best_line = info[0] if isinstance(info, list) else info
                score_obj = best_line["score"].white()

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
                        item_score = str(item.get("score").white()) if "score" in item else ""
                        top_moves.append({
                            "uci": move.uci(),
                            "san": move_san,
                            "score": item_score
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

    async def analyse_for_review(self, board: chess.Board, depth: int = 14) -> Optional[Dict[str, Any]]:
        """
        Engine evaluation for history analysis: {"cp", "mate", "best_move", "depth", "source"} (White POV).
        Returns None when no real engine is reachable - never a material-count guess.
        """
        key = (board.fen(), depth)
        if key in self._review_cache:
            return self._review_cache[key]

        result = None
        if board.is_game_over():
            if board.is_checkmate():
                # The side to move is mated: report it as a decisive score for the other side
                result = {"cp": None, "mate": 1 if board.turn == chess.BLACK else -1, "best_move": None,
                          "depth": depth, "source": "rules"}
            else:
                result = {"cp": 0, "mate": None, "best_move": None, "depth": depth, "source": "rules"}
        elif not board.is_valid():
            # Board position is illegal (e.g. opposite check or impossible king/pawn setup).
            # Do NOT pass to UCI engine as it terminates the process.
            print(f"[EngineManager] Skipping Stockfish analysis for invalid position: {board.fen()}")
        else:
            engine = self._ensure_engine()
            if engine:
                try:
                    info = engine.analyse(board, chess.engine.Limit(depth=depth))
                    score = info["score"].white()
                    pv = info.get("pv") or []
                    result = {
                        "cp": None if score.is_mate() else score.score(),
                        "mate": score.mate() if score.is_mate() else None,
                        "best_move": pv[0].uci() if pv else None,
                        "depth": info.get("depth", depth),
                        "source": "local_stockfish",
                    }
                except Exception as e:
                    print(f"[EngineManager] Review analysis failed: {e}")
        if result is None:
            cloud = await self._fetch_cloud_eval(board.fen())
            if cloud:
                result = {
                    "cp": None if cloud["eval_type"] == "mate" else int(round(cloud["eval_val"] * 100)),
                    "mate": cloud["eval_val"] if cloud["eval_type"] == "mate" else None,
                    "best_move": cloud.get("best_move") or None,
                    "depth": cloud.get("depth"),
                    "source": "lichess_cloud",
                }
        if result is not None:
            if len(self._review_cache) > 20000:
                self._review_cache.clear()
            self._review_cache[key] = result
        return result

    async def get_bot_move(self, board: chess.Board, skill_level: int = 20, target_elo: Optional[int] = None) -> Dict[str, Any]:
        """
        Generates a move for computer opponent based on requested difficulty skill level (0-20) or target ELO rating.
        """
        skill_level = max(0, min(20, skill_level))
        effective_elo = int(target_elo) if (target_elo is not None) else (400 + skill_level * 100)

        engine = self._ensure_engine()
        if engine and board.is_valid():
            try:
                if effective_elo >= 1320:
                    bounded_elo = min(3190, effective_elo)
                    engine.configure({
                        "UCI_LimitStrength": True,
                        "UCI_Elo": bounded_elo,
                        "Skill Level": skill_level
                    })
                    limit = chess.engine.Limit(time=0.25)
                else:
                    # Low ELO (e.g. 400 - 1300): Limit strength + shallow depth limit
                    engine.configure({
                        "UCI_LimitStrength": True,
                        "UCI_Elo": 1320,
                        "Skill Level": max(0, skill_level)
                    })
                    limit = chess.engine.Limit(depth=1, time=0.08)

                result = engine.play(board, limit)
                move = result.move

                # For beginner & intermediate ELO (< 1300), introduce realistic human mistake frequency
                if effective_elo < 1300:
                    legal_moves = list(board.legal_moves)
                    if len(legal_moves) > 1:
                        import random
                        # Graduated blunder / inaccuracy probability curve:
                        # <= 600: 55%, 601-800: 35%, 801-1000: 22%, 1001-1200: 12%, 1201-1299: 6%
                        if effective_elo <= 600:
                            prob_mistake = 0.55
                        elif effective_elo <= 800:
                            prob_mistake = 0.35
                        elif effective_elo <= 1000:
                            prob_mistake = 0.22
                        elif effective_elo <= 1200:
                            prob_mistake = 0.12
                        else:
                            prob_mistake = 0.06

                        if random.random() < prob_mistake:
                            non_top = [m for m in legal_moves if m != move]
                            if non_top:
                                # At 850-1200, pick plausible alternatives; at lower ELO, pick more erratically
                                pool_size = 6 if effective_elo >= 850 else 4
                                move = random.choice(non_top[:min(pool_size, len(non_top))])

                try:
                    self._engine.configure({"UCI_LimitStrength": False, "Skill Level": 20})
                except Exception:
                    pass

                if move:
                    return {
                        "move_uci": move.uci(),
                        "move_san": board.san(move),
                        "skill_level": skill_level,
                        "target_elo": effective_elo,
                        "source": "local_stockfish"
                    }
            except Exception as e:
                print(f"[EngineManager] Bot move generation error: {e}")
                try:
                    self._engine.configure({"UCI_LimitStrength": False, "Skill Level": 20})
                except Exception:
                    pass

        # Fallback using position evaluation candidates
        eval_res = await self.evaluate_position(board, depth=10)
        top_moves = eval_res.get("top_moves", [])
        if top_moves:
            if skill_level < 10 and len(top_moves) > 1:
                import random
                weights = [skill_level + 2, (10 - skill_level) // 2 + 1, (10 - skill_level) // 2]
                chosen = random.choices(top_moves[:len(weights)], weights=weights[:len(top_moves)])[0]
            else:
                chosen = top_moves[0]
            return {
                "move_uci": chosen["uci"],
                "move_san": chosen["san"],
                "skill_level": skill_level,
                "source": eval_res.get("source", "fallback")
            }

        legal_moves = list(board.legal_moves)
        if legal_moves:
            chosen_move = legal_moves[0]
            return {
                "move_uci": chosen_move.uci(),
                "move_san": board.san(chosen_move),
                "skill_level": skill_level,
                "source": "heuristic_fallback"
            }

        return {"move_uci": "", "move_san": "", "skill_level": skill_level, "source": "none"}


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
                        board = chess.Board(fen)
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

        white_score = round(score, 2)
        formatted_score = f"{'+' if white_score > 0 else ''}{white_score}"

        legal_moves = list(board.legal_moves)
        best_uci = legal_moves[0].uci() if legal_moves else ""
        best_san = board.san(legal_moves[0]) if legal_moves else ""

        return {
            "source": "heuristic",
            "score": formatted_score,
            "eval_type": "cp",
            "eval_val": white_score,
            "best_move": best_uci,
            "best_move_san": best_san,
            "top_moves": [{"uci": m.uci(), "san": board.san(m)} for m in legal_moves[:3]],
            "depth": 1
        }
