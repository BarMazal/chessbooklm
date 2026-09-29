import chess
from typing import Dict, Any, Optional, List

# Basic ECO Dictionary for popular openings
ECO_DATABASE = {
    "e2e4 e7e5 f2f4": {
        "name": "King's Gambit",
        "eco": "C30",
        "desc": "An aggressive classical opening aiming for early central dominance and opening the f-file.",
        "continuations": [
            {"move": "e5f4", "san": "exf4", "win": 48, "draw": 22, "loss": 30, "name": "King's Gambit Accepted"},
            {"move": "f8c5", "san": "Bc5", "win": 45, "draw": 28, "loss": 27, "name": "Classical Declined"},
            {"move": "d7d5", "san": "d5", "win": 46, "draw": 26, "loss": 28, "name": "Falkbeer Countergambit"}
        ]
    },
    "e2e4 e7e5 g1f3 b8c6 f1b5": {
        "name": "Ruy Lopez (Spanish Opening)",
        "eco": "C60",
        "desc": "One of the oldest and most deeply analyzed openings, pressuring Black's knight on c6 to control the center.",
        "continuations": [
            {"move": "a7a6", "san": "a6", "win": 48, "draw": 31, "loss": 21, "name": "Morphy Defense"},
            {"move": "g8f6", "san": "Nf6", "win": 46, "draw": 33, "loss": 21, "name": "Berlin Defense"},
            {"move": "f7f5", "san": "f5", "win": 44, "draw": 22, "loss": 34, "name": "Schliemann Gambit"}
        ]
    },
    "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6 f1a4 g8f6": {
        "name": "Ruy Lopez: Morphy Defense",
        "eco": "C78",
        "desc": "Standard main line of Ruy Lopez. Black forces White's bishop to declare its intention while building solid kingside development.",
        "continuations": [
            {"move": "e1g1", "san": "O-O", "win": 50, "draw": 32, "loss": 18, "name": "Closed Main Line"},
            {"move": "d2d3", "san": "d3", "win": 47, "draw": 35, "loss": 18, "name": "Quiet / Anderssen Line"}
        ]
    },
    "e2e4 e7e5 g1f3 b8c6 f1b5 g8f6": {
        "name": "Ruy Lopez: Berlin Defense",
        "eco": "C65",
        "desc": "The solid 'Berlin Wall' famous for high draw rates and resilient defensive structure favored by World Champions.",
        "continuations": [
            {"move": "e1g1", "san": "O-O", "win": 45, "draw": 38, "loss": 17, "name": "Berlin Endgame Line"},
            {"move": "d2d3", "san": "d3", "win": 48, "draw": 34, "loss": 18, "name": "Anti-Berlin"}
        ]
    },
    "e2e4 e7e5 g1f3 b8c6 f1c4": {
        "name": "Italian Game",
        "eco": "C50",
        "desc": "Focuses rapid piece activity on the vulnerable f7 square, allowing sharp tactical lines or quiet positional maneuvering.",
        "continuations": [
            {"move": "f1c5", "san": "Bc5", "win": 47, "draw": 29, "loss": 24, "name": "Giuoco Piano"},
            {"move": "g8f6", "san": "Nf6", "win": 49, "draw": 27, "loss": 24, "name": "Two Knights Defense"}
        ]
    },
    "e2e4 c7c5": {
        "name": "Sicilian Defense",
        "eco": "B20",
        "desc": "The most popular counter-attacking response against 1.e4, creating asymmetrical pawn structures and rich imbalances.",
        "continuations": [
            {"move": "g1f3", "san": "Nf3", "win": 52, "draw": 28, "loss": 20, "name": "Open Sicilian Prep"},
            {"move": "b1c3", "san": "Nc3", "win": 49, "draw": 27, "loss": 24, "name": "Closed Sicilian"},
            {"move": "c2c3", "san": "c3", "win": 50, "draw": 28, "loss": 22, "name": "Alapin Variation"}
        ]
    },
    "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6": {
        "name": "Sicilian Defense: Najdorf Variation",
        "eco": "B90",
        "desc": "Favored by Fischer and Kasparov; a highly sharp tactical variation fighting for queenside expansion and central control.",
        "continuations": [
            {"move": "c1e3", "san": "Be3", "win": 53, "draw": 26, "loss": 21, "name": "English Attack"},
            {"move": "f2f3", "san": "f3", "win": 51, "draw": 28, "loss": 21, "name": "Pragmatic Attack"}
        ]
    },
    "e2e4 e7e6": {
        "name": "French Defense",
        "eco": "C00",
        "desc": "A solid, resilient defense where Black yields central space in exchange for a sturdy pawn chain target on d4.",
        "continuations": [
            {"move": "d2d4", "san": "d4", "win": 51, "draw": 27, "loss": 22, "name": "Main Line French"},
            {"move": "d2d3", "san": "d3", "win": 48, "draw": 29, "loss": 23, "name": "King's Indian Attack Setup"}
        ]
    },
    "e2e4 c7c6": {
        "name": "Caro-Kann Defense",
        "eco": "B10",
        "desc": "An extremely solid defense preparing d5 without blocking the light-squared bishop on c8.",
        "continuations": [
            {"move": "d2d4", "san": "d4", "win": 50, "draw": 30, "loss": 20, "name": "Main Line Caro-Kann"},
            {"move": "b1c3", "san": "Nc3", "win": 49, "draw": 28, "loss": 23, "name": "Two Knights Variation"}
        ]
    },
    "d2d4 d7d5 c2c4": {
        "name": "Queen's Gambit",
        "eco": "D06",
        "desc": "White offers a wing pawn to capture absolute control over the center with e4.",
        "continuations": [
            {"move": "e7e6", "san": "e6", "win": 49, "draw": 33, "loss": 18, "name": "Queen's Gambit Declined"},
            {"move": "c7c6", "san": "c6", "win": 48, "draw": 32, "loss": 20, "name": "Slav Defense"},
            {"move": "d5c4", "san": "dxc4", "win": 52, "draw": 26, "loss": 22, "name": "Queen's Gambit Accepted"}
        ]
    },
    "d2d4 g8f6 c2c4 g7g6": {
        "name": "King's Indian / Indian Defense",
        "eco": "E60",
        "desc": "Hypermodern defense where Black allows White central pawns, intending to break them down with e5 or c5 later.",
        "continuations": [
            {"move": "b1c3", "san": "Nc3", "win": 52, "draw": 29, "loss": 19, "name": "Classical Main Line"},
            {"move": "g2g3", "san": "g3", "win": 50, "draw": 32, "loss": 18, "name": "Fianchetto Variation"}
        ]
    }
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
        info = ChessTranslator.get_opening_info(board)
        return info["name"]

    @staticmethod
    def get_opening_info(board: chess.Board) -> Dict[str, Any]:
        """
        Returns full ECO dictionary entry for board move sequence.
        """
        moves_str = " ".join([m.uci() for m in board.move_stack])
        
        matched_opening = {
            "name": "Standard Position / Open Game",
            "eco": "A00",
            "desc": "Standard starting position or non-standard opening moves.",
            "continuations": []
        }
        max_len = 0
        for seq, entry in ECO_DATABASE.items():
            if moves_str.startswith(seq) and len(seq) > max_len:
                if isinstance(entry, dict):
                    matched_opening = entry
                else:
                    matched_opening = {"name": entry, "eco": "A00", "desc": "", "continuations": []}
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

SPECIAL FORMATTING INSTRUCTIONS:
Always conclude your response with a dedicated section formatted exactly as:
💡 GENERALIZED TURN RULE:
Followed by a single, high-level, re-usable strategic chess rule derived from this position (e.g., "When opponent overextends queenside pawns, target the base of the chain with counter-levers", "In open positions, coordinate rooks on open files").
CRITICAL: The Generalized Turn Rule MUST be a general strategic principle applicable across multiple games. Do NOT state specific move notation (like 7...Na5 8.e3 c6) in the Generalized Turn Rule.
"""
        return prompt.strip()

    @classmethod
    def analyze_board_positional_overlays(cls, board: chess.Board) -> List[Dict[str, Any]]:
        """
        Analyzes 64 squares for positional elements: outposts, weak squares/holes, targets, open columns, active pieces.
        Returns a list of structured overlay items for White and Black.
        """
        overlays = []
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        white_pawn_attacks = set()
        black_pawn_attacks = set()
        for sq, piece in board.piece_map().items():
            if piece.piece_type == chess.PAWN:
                attacks = board.attacks(sq)
                if piece.color == chess.WHITE:
                    white_pawn_attacks.update(attacks)
                else:
                    black_pawn_attacks.update(attacks)

        def can_pawn_guard(color: chess.Color, target_sq: int) -> bool:
            f_idx = chess.square_file(target_sq)
            r_idx = chess.square_rank(target_sq)
            adj_files = [f for f in [f_idx - 1, f_idx + 1] if 0 <= f <= 7]
            for sq, piece in board.piece_map().items():
                if piece.piece_type == chess.PAWN and piece.color == color:
                    p_file = chess.square_file(sq)
                    p_rank = chess.square_rank(sq)
                    if p_file in adj_files:
                        if color == chess.WHITE and p_rank < r_idx:
                            return True
                        elif color == chess.BLACK and p_rank > r_idx:
                            return True
            return False

        for sq, piece in board.piece_map().items():
            sq_name = chess.square_name(sq)
            r_idx = chess.square_rank(sq)
            f_idx = chess.square_file(sq)
            piece_color_name = "white" if piece.color == chess.WHITE else "black"
            enemy_color = chess.BLACK if piece.color == chess.WHITE else chess.WHITE

            if piece.piece_type in (chess.KNIGHT, chess.BISHOP):
                is_advanced = (piece.color == chess.WHITE and r_idx in (3, 4, 5)) or (piece.color == chess.BLACK and r_idx in (2, 3, 4))
                is_defended_by_pawn = (piece.color == chess.WHITE and sq in white_pawn_attacks) or (piece.color == chess.BLACK and sq in black_pawn_attacks)
                cannot_be_attacked_by_enemy_pawn = not can_pawn_guard(enemy_color, sq)

                if is_advanced and is_defended_by_pawn and cannot_be_attacked_by_enemy_pawn:
                    piece_char = "N" if piece.piece_type == chess.KNIGHT else "B"
                    overlays.append({
                        "square": sq_name,
                        "side": piece_color_name,
                        "color": piece_color_name,
                        "category": "good",
                        "type": "outpost",
                        "badge": "🏰",
                        "icon": "🏰",
                        "title": f"{piece_color_name.capitalize()} Outpost ({piece_char}{sq_name})",
                        "tooltip": f"{piece_color_name.capitalize()}: Strong {piece_color_name} {chess.piece_name(piece.piece_type)} outpost on {sq_name}, defended by pawn and unassailable by enemy pawns.",
                        "text": f"{piece_color_name.capitalize()}: Strong {piece_color_name} {chess.piece_name(piece.piece_type)} outpost on {sq_name}, defended by pawn and unassailable by enemy pawns."
                    })

            PIECE_VALUES = {
                chess.PAWN: 1,
                chess.KNIGHT: 3,
                chess.BISHOP: 3,
                chess.ROOK: 5,
                chess.QUEEN: 9,
                chess.KING: 0
            }

            is_attacked_by_enemy = board.is_attacked_by(enemy_color, sq)
            is_defended_by_friendly = board.is_attacked_by(piece.color, sq)
            
            has_lower_value_attacker = False
            if is_attacked_by_enemy:
                enemy_attackers = board.attackers(enemy_color, sq)
                piece_val = PIECE_VALUES.get(piece.piece_type, 0)
                for att_sq in enemy_attackers:
                    att_piece = board.piece_at(att_sq)
                    if att_piece and PIECE_VALUES.get(att_piece.piece_type, 0) < piece_val:
                        has_lower_value_attacker = True
                        break

            if is_attacked_by_enemy and (not is_defended_by_friendly or has_lower_value_attacker):
                p_name = chess.piece_name(piece.piece_type).capitalize()
                reason = "attacked by lower-value piece" if has_lower_value_attacker else "undefended and under attack"
                overlays.append({
                    "square": sq_name,
                    "side": piece_color_name,
                    "color": piece_color_name,
                    "category": "weak",
                    "type": "target",
                    "badge": "🎯",
                    "icon": "🎯",
                    "title": f"{piece_color_name.capitalize()} {p_name} Target ({sq_name})",
                    "tooltip": f"{piece_color_name.capitalize()}: {piece_color_name.capitalize()} {p_name} on {sq_name} is {reason}!",
                    "text": f"{piece_color_name.capitalize()}: {piece_color_name.capitalize()} {p_name} on {sq_name} is {reason}!"
                })

            if piece.piece_type in (chess.ROOK, chess.QUEEN):
                pawns_on_file = [p for s, p in board.piece_map().items() if chess.square_file(s) == f_idx and p.piece_type == chess.PAWN]
                if len(pawns_on_file) == 0:
                    overlays.append({
                        "square": sq_name,
                        "side": piece_color_name,
                        "color": piece_color_name,
                        "category": "good",
                        "type": "open_file",
                        "badge": "🔋",
                        "icon": "🔋",
                        "title": f"{piece_color_name.capitalize()} Open File Control ({files[f_idx]}-file)",
                        "tooltip": f"{piece_color_name.capitalize()}: {chess.piece_name(piece.piece_type).capitalize()} on {sq_name} controlling open {files[f_idx]}-file.",
                        "text": f"{piece_color_name.capitalize()}: {chess.piece_name(piece.piece_type).capitalize()} on {sq_name} controlling open {files[f_idx]}-file."
                    })

        for sq in chess.SQUARES:
            if board.piece_at(sq) is None:
                sq_name = chess.square_name(sq)
                r_idx = chess.square_rank(sq)

                if r_idx in (2, 3, 4):
                    if board.is_attacked_by(chess.BLACK, sq) and not can_pawn_guard(chess.WHITE, sq):
                        overlays.append({
                            "square": sq_name,
                            "side": "white",
                            "color": "white",
                            "category": "weak",
                            "type": "weak_square",
                            "badge": "🛡️",
                            "icon": "🛡️",
                            "title": f"White Weak Square Hole ({sq_name})",
                            "tooltip": f"White: Weak square hole on {sq_name} controlled by Black that cannot be defended by White pawns.",
                            "text": f"White: Weak square hole on {sq_name} controlled by Black that cannot be defended by White pawns."
                        })

                if r_idx in (5, 4, 3):
                    if board.is_attacked_by(chess.WHITE, sq) and not can_pawn_guard(chess.BLACK, sq):
                        overlays.append({
                            "square": sq_name,
                            "side": "black",
                            "color": "black",
                            "category": "weak",
                            "type": "weak_square",
                            "badge": "🛡️",
                            "icon": "🛡️",
                            "title": f"Black Weak Square Hole ({sq_name})",
                            "tooltip": f"Black: Weak square hole on {sq_name} controlled by White that cannot be defended by Black pawns.",
                            "text": f"Black: Weak square hole on {sq_name} controlled by White that cannot be defended by Black pawns."
                        })

        return overlays

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
