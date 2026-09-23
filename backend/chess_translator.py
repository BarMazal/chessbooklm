import chess
from typing import Dict, Any, Optional

# Basic ECO Dictionary for popular openings
ECO_DATABASE = {
    "e2e4 e7e5 f2f4": "King's Gambit",
    "e2e4 e7e5 g1f3 b8c6 f1b5": "Ruy Lopez (Spanish Opening)",
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 f1a4 g8f6": "Ruy Lopez: Morphy Defense",
    "e2e4 e7e5 g1f3 b8c6 f1b5 g8f6": "Ruy Lopez: Berlin Defense",
    "e2e4 e7e5 g1f3 b8c6 f1c4": "Italian Game",
    "e2e4 c7c5": "Sicilian Defense",
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6": "Sicilian Defense: Najdorf Variation",
    "e2e4 c7c5 g1f3 e7e6": "Sicilian Defense: French Variation",
    "e2e4 e7e6": "French Defense",
    "e2e4 c7c6": "Caro-Kann Defense",
    "d2d4 d7d5 c2c4": "Queen's Gambit",
    "d2d4 d7d5 c2c4 e7e6": "Queen's Gambit Declined",
    "d2d4 d7d5 c2c4 c7c6": "Slav Defense",
    "d2d4 g8f6 c2c4 g7g6": "King's Indian / Indian Defense",
}

class ChessTranslator:
    """
    Translates raw chess board state, FEN, PGN, and Stockfish analysis
    into natural human text for NotebookLM / Gemini grounding.
    """

    @staticmethod
    def identify_opening(board: chess.Board) -> str:
        """
        Matches move history against ECO opening dictionary.
        """
        moves_str = " ".join([m.uci() for m in board.move_stack])
        
        # Match longest matching move sequence first
        matched_opening = "Standard Position / Open Game"
        max_len = 0
        for seq, name in ECO_DATABASE.items():
            if moves_str.startswith(seq) and len(seq) > max_len:
                matched_opening = name
                max_len = len(seq)

        return matched_opening

    @staticmethod
    def get_tactical_summary(board: chess.Board) -> Dict[str, Any]:
        """
        Extracts attacked pieces, checks, king safety, and material values.
        """
        turn = "White" if board.turn == chess.WHITE else "Black"
        opponent = "Black" if board.turn == chess.WHITE else "White"

        is_check = board.is_check()
        is_checkmate = board.is_checkmate()
        is_stalemate = board.is_stalemate()

        # Find pieces under attack for side to move
        under_attack = []
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == board.turn:
                if board.is_attacked_by(not board.turn, square):
                    p_name = chess.piece_name(piece.piece_type).capitalize()
                    sq_name = chess.square_name(square)
                    under_attack.append(f"{p_name} on {sq_name}")

        return {
            "turn": turn,
            "opponent": opponent,
            "is_check": is_check,
            "is_checkmate": is_checkmate,
            "is_stalemate": is_stalemate,
            "under_attack": under_attack
        }

    @classmethod
    def translate_position_to_human(
        cls, 
        board: chess.Board, 
        eval_data: Dict[str, Any],
        user_question: Optional[str] = None
    ) -> str:
        """
        Converts board state and Stockfish analysis into a rich, natural language prompt.
        """
        turn = "White" if board.turn == chess.WHITE else "Black"
        opening_name = cls.identify_opening(board)
        tactics = cls.get_tactical_summary(board)

        # 1. Translate Evaluation
        eval_type = eval_data.get("eval_type", "cp")
        eval_val = eval_data.get("eval_val", 0.0)
        score_str = eval_data.get("score", "0.0")

        if eval_type == "mate":
            mate_moves = abs(int(eval_val))
            side = "White" if eval_val > 0 else "Black"
            eval_desc = f"a forced checkmate in {mate_moves} move(s) for {side}"
        else:
            abs_score = abs(eval_val)
            if abs_score <= 0.4:
                eval_desc = "a completely balanced and equal game"
            elif abs_score <= 1.0:
                side = "White" if eval_val > 0 else "Black"
                eval_desc = f"a slight edge for {side}"
            elif abs_score <= 2.5:
                side = "White" if eval_val > 0 else "Black"
                eval_desc = f"a clear, solid advantage for {side}"
            else:
                side = "White" if eval_val > 0 else "Black"
                eval_desc = f"a overwhelming winning position for {side}"

        # 2. Best Engine Suggestion
        best_move_uci = eval_data.get("best_move", "")
        best_move_desc = "None"
        if best_move_uci and len(best_move_uci) >= 4:
            try:
                move_obj = chess.Move.from_uci(best_move_uci)
                piece = board.piece_at(move_obj.from_square)
                piece_name = chess.piece_name(piece.piece_type).capitalize() if piece else "Piece"
                from_sq = chess.square_name(move_obj.from_square)
                to_sq = chess.square_name(move_obj.to_square)
                is_cap = board.is_capture(move_obj)
                cap_text = f"captures on {to_sq}" if is_cap else f"moves to {to_sq}"
                san_move = eval_data.get("best_move_san", board.san(move_obj))
                best_move_desc = f"{piece_name} on {from_sq} {cap_text} ({san_move})"
            except Exception:
                best_move_desc = best_move_uci

        # 3. Kings & Threats Status
        status_lines = []
        if tactics["is_check"]:
            status_lines.append(f"CRITICAL: {turn}'s King is currently in CHECK!")
        if tactics["under_attack"]:
            status_lines.append(f"Pieces under direct threat: {', '.join(tactics['under_attack'])}.")
        else:
            status_lines.append("No major pieces are under immediate undefended threat.")

        status_text = " ".join(status_lines)

        # 4. Construct Structured Mentor Prompt
        prompt = f"""CHESS POSITION CONTEXT:
- Active Turn: {turn} to move.
- Identified Opening: {opening_name}
- Stockfish Engine Evaluation: {eval_desc} (Raw Score: {score_str}).
- King & Tactical Status: {status_text}
- Top Recommended Move by Engine: {best_move_desc}.

BOARD FEN: {board.fen()}
MOVE HISTORY: {' '.join([m.uci() for m in board.move_stack]) if board.move_stack else 'Starting Position'}

USER QUERY / DISCUSSION ITEM:
{user_question or f"Explain why Stockfish recommends {best_move_desc} for {turn}, what strategic themes exist in this {opening_name} position, and what main plans both sides should pursue."}
"""
        return prompt.strip()

    @classmethod
    def translate_raw_fen_mode(cls, fen: str, user_question: Optional[str] = None) -> str:
        """
        Direct Raw FEN mode prompt for testing NotebookLM's native chess notation comprehension.
        """
        return f"""CHESS FEN QUERY:
The current position in FEN notation is:
{fen}

Question:
{user_question or "What is the strategic evaluation, best plan, and opening advice for this position?"}
"""
