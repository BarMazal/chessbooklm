"""
Per-move and per-sequence analysis for history DAG nodes (schema v2).

Everything here is derived from the board and from real engine evaluations.
Nothing is filled in with template text: when an input is missing (no engine,
no previous position) the matching field is null.

Node analysis layout (one copy of everything):

    {
      "schema_version": 2,
      "context":  {phase, opening: {eco, name, is_book_move}, move_number, fen_before, fen_after},
      "engine":   {eval_before, eval_after, mate_before, mate_after, score_before, score_after,
                   eval_delta, cp_loss, win_prob_before, win_prob_after, best_move_uci,
                   best_move_san, played_is_best, quality, missed_opportunity, depth, source},
      "move":     {aspects: {6 scores 0-100}, motifs_for: [...], motifs_against: [...],
                   primary_motif, category},
      "sequence": {...}  (see build_sequence_analysis)
      "mentor":   {...}  (written by the NotebookLM mentor only)
    }

Motif entries look like {"id": "fork", "score": 72, "status": "created", "detail": "Nd5 attacks Qc7, Rf6"}.
- motifs_for:     patterns the mover CREATED with this move (they did not exist before it).
- motifs_against: opportunities the opponent HAS after this move, either created by
                  this move ("allowed") or already there and left unaddressed ("ignored").
Scores are 0-100. The primary motif is the highest-scoring entry of both lists.

The six aspects (0-100, from the mover's point of view):
- building_state:      positional motifs created + mobility gained (+ development/castling in the opening).
- seizing_opportunity: strongest tactical motif created, or material won with the engine's best move.
- score:               material yielded by the move itself (capture/promotion/mate).
- preventing_opponent_building_state: opponent mobility removed + opponent patterns dismantled.
- avoiding_opponent_seizing_opportunity: 100 minus the worst tactical chance handed to the opponent
                       (or the engine's cp loss, whichever is worse).
- opponent_score:      winning chances handed to the opponent (win-probability drop x2).
"""
import math
from typing import Any, Dict, List, Optional, Tuple

import chess

from backend.chess_translator import ECO_DATABASE, ChessTranslator

VALUES = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
TARGET_VALUES = {**VALUES, chess.KING: 9}  # how much a king "counts" as a fork/skewer target
MATE_CP = 1000  # mate scores are clamped to +-10 pawns for deltas and win probability

TACTICAL_MOTIFS = {
    "fork", "pin", "skewer", "discovered_attack", "hanging_piece", "back_rank",
    "mate_threat", "overloaded_defender", "trapped_piece",
}
# Opponent threats that count against the mover even when they existed before the move
# (the mover had the chance to deal with them and did not).
IGNORABLE_THREATS = {"hanging_piece", "fork", "mate_threat", "back_rank", "trapped_piece", "skewer"}

MOTIF_INFO = {
    "fork": {"label": "Fork / Double Attack",
             "for": "One piece attacks two or more valuable or undefended targets.",
             "against": "Allowing a single enemy piece to attack two of your pieces at once."},
    "pin": {"label": "Pin",
            "for": "A piece is pinned to its king or to a more valuable piece.",
            "against": "Walking into (or leaving) a pin against your pieces."},
    "skewer": {"label": "Skewer",
               "for": "A valuable piece is attacked with a lesser piece exposed behind it.",
               "against": "Lining up valuable pieces on an open enemy line."},
    "discovered_attack": {"label": "Discovered Attack",
                          "for": "Moving a piece opens a line for another attacker (discovered check/attack).",
                          "against": "Overlooking an enemy discovered attack."},
    "hanging_piece": {"label": "Hanging Piece",
                      "for": "Attacking an undefended piece or one defended only by a cheaper attacker.",
                      "against": "Leaving a piece undefended or attacked by a cheaper enemy piece."},
    "back_rank": {"label": "Back-Rank Threat",
                  "for": "A rook or queen hits the enemy back rank: mate, a check that wins material, or a check on a boxed-in king.",
                  "against": "Allowing back-rank mates or back-rank checks that win material against your king."},
    "mate_threat": {"label": "Mate Threat",
                    "for": "Threatening checkmate in one.",
                    "against": "Allowing the opponent a mate-in-one."},
    "overloaded_defender": {"label": "Overloaded Defender",
                            "for": "One enemy piece is the only defender of two attacked pieces.",
                            "against": "Relying on one piece to defend two attacked pieces."},
    "trapped_piece": {"label": "Trapped Piece",
                      "for": "An enemy piece is attacked and has no safe square.",
                      "against": "Putting a piece where it is attacked with no safe retreat."},
    "battery": {"label": "Battery",
                "for": "Two long-range pieces lined up on the same file, rank or diagonal.",
                "against": "Allowing the opponent to double up pieces on an open line."},
    "passed_pawn": {"label": "Passed Pawn",
                    "for": "Creating or advancing a pawn no enemy pawn can stop.",
                    "against": "Allowing the opponent a new or advanced passed pawn."},
    "outpost": {"label": "Outpost",
                "for": "A knight or bishop on an advanced square no enemy pawn can attack.",
                "against": "Allowing an enemy piece to settle on an outpost."},
    "open_file": {"label": "Open File",
                  "for": "A rook or queen takes an open or semi-open file.",
                  "against": "Yielding an open file to enemy rooks or queen."},
    "seventh_rank": {"label": "Seventh-Rank Invasion",
                     "for": "A rook or queen invades the opponent's second rank.",
                     "against": "Allowing an enemy rook or queen onto your second rank."},
    "exposed_king": {"label": "King Exposure",
                     "for": "",
                     "against": "Weakening the pawn shield in front of your own king."},
    "pawn_weakness": {"label": "Pawn Structure Weakness",
                      "for": "",
                      "against": "Creating doubled or isolated pawns in your own structure."},
    "simplification": {"label": "Simplification When Ahead",
                       "for": "Trading pieces while ahead to head for a winning endgame.",
                       "against": ""},
}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def _as_side(board: chess.Board, side: chess.Color) -> chess.Board:
    """Copy of the board with `side` to move (null move if needed), for threat detection."""
    b = board.copy(stack=False)
    if b.turn != side:
        b.push(chess.Move.null())
    return b


def _name(board: chess.Board, sq: int) -> str:
    p = board.piece_at(sq)
    if not p:
        return chess.square_name(sq)
    letter = p.symbol().upper() if p.piece_type != chess.PAWN else ""
    return f"{letter}{chess.square_name(sq)}"


def _hanging_gain(board: chess.Board, sq: int) -> int:
    """Material an attacker wins by taking the piece on sq (0 if it is not hanging)."""
    p = board.piece_at(sq)
    if not p or p.piece_type == chess.KING:
        return 0
    attackers = board.attackers(not p.color, sq)
    if not attackers:
        return 0
    val = VALUES[p.piece_type]
    if not board.attackers(p.color, sq):
        return val
    cheapest = min(VALUES[board.piece_at(a).piece_type] or 100 for a in attackers)
    return max(0, val - cheapest)


def _ray_beyond(origin: int, target: int) -> List[int]:
    """Squares past `target` on the line from origin through target."""
    df = chess.square_file(target) - chess.square_file(origin)
    dr = chess.square_rank(target) - chess.square_rank(origin)
    if not (df == 0 or dr == 0 or abs(df) == abs(dr)):
        return []
    sf = (df > 0) - (df < 0)
    sr = (dr > 0) - (dr < 0)
    out = []
    f, r = chess.square_file(target) + sf, chess.square_rank(target) + sr
    while 0 <= f <= 7 and 0 <= r <= 7:
        out.append(chess.square(f, r))
        f += sf
        r += sr
    return out


def _first_piece(board: chess.Board, squares: List[int]) -> Optional[int]:
    for s in squares:
        if board.piece_at(s):
            return s
    return None


def _clamp(v: float, lo: float = 0, hi: float = 100) -> int:
    return int(round(max(lo, min(hi, v))))


def _mobility(board: chess.Board, side: chess.Color) -> int:
    return _as_side(board, side).legal_moves.count()


def _can_be_hit_by_pawn(board: chess.Board, sq: int, pawn_color: chess.Color) -> bool:
    """True if a pawn of pawn_color could ever attack sq (adjacent file, behind it)."""
    f, r = chess.square_file(sq), chess.square_rank(sq)
    for p_sq in board.pieces(chess.PAWN, pawn_color):
        pf, pr = chess.square_file(p_sq), chess.square_rank(p_sq)
        if abs(pf - f) == 1 and ((pawn_color == chess.WHITE and pr < r) or (pawn_color == chess.BLACK and pr > r)):
            return True
    return False


# ---------------------------------------------------------------------------
# Motif detectors: each returns {key: (motif_id, score, detail)} for side S
# ---------------------------------------------------------------------------
def detect_opportunities(board: chess.Board, side: chess.Color) -> Dict[Tuple, Tuple[str, int, str]]:
    found: Dict[Tuple, Tuple[str, int, str]] = {}
    enemy = not side
    b = _as_side(board, side)

    # Hanging enemy pieces
    for sq, p in b.piece_map().items():
        if p.color == enemy:
            gain = _hanging_gain(b, sq)
            if gain > 0:
                found[("hanging_piece", sq)] = ("hanging_piece", _clamp(30 + gain * 10),
                                                f"{_name(b, sq)} can be won (+{gain})")

    # Forks
    for sq, p in b.piece_map().items():
        if p.color != side:
            continue
        att_val = VALUES[p.piece_type] or 100
        targets = []
        for t in b.attacks(sq):
            tp = b.piece_at(t)
            if tp and tp.color == enemy:
                if tp.piece_type == chess.KING or VALUES[tp.piece_type] > att_val or not b.attackers(enemy, t):
                    targets.append(t)
        if len(targets) >= 2:
            vals = sorted((TARGET_VALUES[b.piece_at(t).piece_type] for t in targets), reverse=True)
            score = 45 + 5 * sum(vals[:2])
            if _hanging_gain(b, sq) > 0:  # the forking piece can simply be taken
                score *= 0.5
            found[("fork", sq)] = ("fork", _clamp(score),
                                   f"{_name(b, sq)} attacks " + ", ".join(_name(b, t) for t in targets))

    # Pins, skewers (sliders only)
    enemy_king = b.king(enemy)
    for sq, p in b.piece_map().items():
        if p.color != side or p.piece_type not in (chess.BISHOP, chess.ROOK, chess.QUEEN):
            continue
        for t in b.attacks(sq):
            tp = b.piece_at(t)
            if not tp or tp.color != enemy:
                continue
            behind_sq = _first_piece(b, _ray_beyond(sq, t))
            behind = b.piece_at(behind_sq) if behind_sq is not None else None
            if not behind or behind.color != enemy:
                continue
            front_v, back_v = TARGET_VALUES[tp.piece_type], TARGET_VALUES[behind.piece_type]
            if behind_sq == enemy_king and tp.piece_type != chess.KING:
                found[("pin", sq, t)] = ("pin", _clamp(40 + 4 * VALUES[tp.piece_type]),
                                         f"{_name(b, t)} pinned to the king by {_name(b, sq)}")
            elif tp.piece_type != chess.KING and back_v > front_v and back_v > VALUES[p.piece_type]:
                found[("pin", sq, t)] = ("pin", _clamp(30 + 3 * back_v),
                                         f"{_name(b, t)} pinned to {_name(b, behind_sq)} by {_name(b, sq)}")
            elif front_v > back_v and (front_v >= 5) and (back_v >= 3 or not b.attackers(enemy, behind_sq)):
                found[("skewer", sq, t)] = ("skewer", _clamp(40 + 4 * VALUES[behind.piece_type]),
                                            f"{_name(b, sq)} skewers {_name(b, t)} with {_name(b, behind_sq)} behind")

    # Mate in one, and back-rank threats (mate, or a rook/queen check on the back rank that
    # wins material or leaves the king stuck on that rank)
    king_sq = b.king(enemy)
    back_rank = 0 if enemy == chess.WHITE else 7
    king_on_back = king_sq is not None and chess.square_rank(king_sq) == back_rank
    for m in list(b.legal_moves):
        piece = b.piece_at(m.from_square)
        captured = b.piece_at(m.to_square)
        san = b.san(m)
        b.push(m)
        mate = b.is_checkmate()
        check = b.is_check()
        boxed = False
        if check and not mate and king_on_back:
            king_moves = [km for km in b.legal_moves if km.from_square == king_sq]
            boxed = all(chess.square_rank(km.to_square) == back_rank for km in king_moves)
        b.pop()
        on_back_rank = (piece and piece.piece_type in (chess.ROOK, chess.QUEEN) and king_on_back
                        and chess.square_rank(m.to_square) == back_rank)
        score, detail = 0, ""
        if on_back_rank and mate:
            score, detail = 95, f"{san} mates on the back rank"
        elif on_back_rank and check and captured:
            score, detail = _clamp(55 + 4 * VALUES[captured.piece_type]), f"{san} wins material with a back-rank check"
        elif on_back_rank and check and boxed:
            score, detail = 45, f"{san} checks a king boxed in on the back rank"
        elif mate:
            found[("mate_threat", m.to_square)] = ("mate_threat", 95, f"{san} is mate")
        if score:
            key = ("back_rank", m.to_square)
            if key not in found or found[key][1] < score:
                found[key] = ("back_rank", score, detail)

    # Overloaded defender: one enemy piece is the only defender of 2+ attacked pieces
    sole_defender_of: Dict[int, List[int]] = {}
    for sq, p in b.piece_map().items():
        if p.color != enemy or p.piece_type == chess.KING or not b.attackers(side, sq):
            continue
        defenders = list(b.attackers(enemy, sq))
        if len(defenders) == 1:
            sole_defender_of.setdefault(defenders[0], []).append(sq)
    for d, guarded in sole_defender_of.items():
        if len(guarded) >= 2:
            found[("overloaded_defender", d)] = ("overloaded_defender", 55,
                                                 f"{_name(b, d)} alone guards " + ", ".join(_name(b, g) for g in guarded))

    # Trapped enemy piece: attacked by something cheaper/undefended, and every escape is unsafe
    eb = _as_side(board, enemy)
    for sq, p in eb.piece_map().items():
        if p.color != enemy or p.piece_type in (chess.PAWN, chess.KING):
            continue
        if _hanging_gain(eb, sq) <= 0:
            continue
        safe_escape = False
        for m in eb.legal_moves:
            if m.from_square != sq:
                continue
            eb.push(m)
            if _hanging_gain(eb, m.to_square) <= 0:
                safe_escape = True
            eb.pop()
            if safe_escape:
                break
        if not safe_escape:
            found[("trapped_piece", sq)] = ("trapped_piece", _clamp(30 + 5 * VALUES[p.piece_type]),
                                            f"{_name(eb, sq)} has no safe square")

    # --- positional patterns ---
    # Battery: two friendly sliders adjacent on one line, with compatible movement
    for sq, p in b.piece_map().items():
        if p.color != side or p.piece_type not in (chess.BISHOP, chess.ROOK, chess.QUEEN):
            continue
        for t in b.attacks(sq):
            tp = b.piece_at(t)
            if not tp or tp.color != side or tp.piece_type not in (chess.BISHOP, chess.ROOK, chess.QUEEN):
                continue
            diagonal = chess.square_file(sq) != chess.square_file(t) and chess.square_rank(sq) != chess.square_rank(t)
            ok_types = {chess.BISHOP, chess.QUEEN} if diagonal else {chess.ROOK, chess.QUEEN}
            if p.piece_type in ok_types and tp.piece_type in ok_types:
                key = ("battery",) + tuple(sorted((sq, t)))
                found[key] = ("battery", 30, f"{_name(b, sq)} and {_name(b, t)} lined up")

    for sq in b.pieces(chess.PAWN, side):
        if ChessTranslator.is_passed_pawn(b, sq, side):
            rel_rank = chess.square_rank(sq) if side == chess.WHITE else 7 - chess.square_rank(sq)
            found[("passed_pawn", sq)] = ("passed_pawn", _clamp(25 + 10 * max(0, rel_rank - 3)),
                                          f"passed pawn on {chess.square_name(sq)}")

    own_pawn_attacks = set()
    for p_sq in b.pieces(chess.PAWN, side):
        own_pawn_attacks.update(b.attacks(p_sq))
    for sq, p in b.piece_map().items():
        if p.color != side or p.piece_type not in (chess.KNIGHT, chess.BISHOP):
            continue
        rel_rank = chess.square_rank(sq) if side == chess.WHITE else 7 - chess.square_rank(sq)
        if rel_rank in (3, 4, 5) and sq in own_pawn_attacks and not _can_be_hit_by_pawn(b, sq, enemy):
            found[("outpost", sq)] = ("outpost", 35 if p.piece_type == chess.KNIGHT else 25,
                                      f"{_name(b, sq)} on an outpost")

    for sq, p in b.piece_map().items():
        if p.color != side or p.piece_type not in (chess.ROOK, chess.QUEEN):
            continue
        f = chess.square_file(sq)
        file_pawns = [s for s in chess.SquareSet(chess.BB_FILES[f]) if b.piece_type_at(s) == chess.PAWN]
        own_on_file = [s for s in file_pawns if b.color_at(s) == side]
        if not file_pawns:
            found[("open_file", sq)] = ("open_file", 35 if p.piece_type == chess.ROOK else 20,
                                        f"{_name(b, sq)} on the open {chess.FILE_NAMES[f]}-file")
        elif not own_on_file:
            found[("open_file", sq)] = ("open_file", 20,
                                        f"{_name(b, sq)} on the semi-open {chess.FILE_NAMES[f]}-file")
        seventh = 6 if side == chess.WHITE else 1
        if chess.square_rank(sq) == seventh:
            rank_targets = [s for s in chess.SquareSet(chess.BB_RANKS[seventh]) if b.color_at(s) == enemy]
            king_sq = b.king(enemy)
            king_back = king_sq is not None and chess.square_rank(king_sq) == (7 if side == chess.WHITE else 0)
            if rank_targets or king_back:
                found[("seventh_rank", sq)] = ("seventh_rank", 40, f"{_name(b, sq)} on the seventh rank")

    return found


def _discovered_attacks(before: chess.Board, after: chess.Board, move: chess.Move, mover: chess.Color) -> List[Dict[str, Any]]:
    """Attacks revealed by the moved piece leaving its square (the slider itself did not move)."""
    out = []
    enemy = not mover
    for sq, p in after.piece_map().items():
        if p.color != mover or sq == move.to_square or p.piece_type not in (chess.BISHOP, chess.ROOK, chess.QUEEN):
            continue
        new_targets = [t for t in after.attacks(sq) if after.color_at(t) == enemy and t not in before.attacks(sq)
                       and move.from_square in chess.SquareSet.between(sq, t)]
        for t in new_targets:
            tp = after.piece_at(t)
            if tp.piece_type == chess.KING:
                out.append({"id": "discovered_attack", "score": 85,
                            "detail": f"discovered check by {_name(after, sq)}"})
            elif VALUES[tp.piece_type] >= VALUES[p.piece_type] or not after.attackers(enemy, t):
                out.append({"id": "discovered_attack", "score": _clamp(40 + 4 * VALUES[tp.piece_type]),
                            "detail": f"{_name(after, sq)} now attacks {_name(after, t)}"})
    return out


def _king_shield(board: chess.Board, color: chess.Color) -> int:
    k = board.king(color)
    if k is None:
        return 0
    kf, kr = chess.square_file(k), chess.square_rank(k)
    step = 1 if color == chess.WHITE else -1
    count = 0
    for dr in (1, 2):
        r = kr + step * dr
        for f in (kf - 1, kf, kf + 1):
            if 0 <= f <= 7 and 0 <= r <= 7:
                p = board.piece_at(chess.square(f, r))
                if p and p.piece_type == chess.PAWN and p.color == color:
                    count += 1
    return count


def _pawn_weakness_count(board: chess.Board, color: chess.Color) -> int:
    files = [chess.square_file(s) for s in board.pieces(chess.PAWN, color)]
    doubled = sum(files.count(f) - 1 for f in set(files) if files.count(f) > 1)
    isolated = sum(1 for f in files if (f - 1) not in files and (f + 1) not in files)
    return doubled + isolated


def _merge_motifs(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Keep the strongest entry per motif id, sorted by score."""
    best: Dict[str, Dict[str, Any]] = {}
    for it in items:
        if it["score"] <= 0:
            continue
        cur = best.get(it["id"])
        if not cur or it["score"] > cur["score"]:
            best[it["id"]] = it
    return sorted(best.values(), key=lambda x: -x["score"])


# ---------------------------------------------------------------------------
# Engine numbers
# ---------------------------------------------------------------------------
def win_prob(cp_white: float, color: chess.Color) -> float:
    """Winning chances (0-100) for `color`, Lichess logistic model."""
    cp = cp_white if color == chess.WHITE else -cp_white
    cp = max(-MATE_CP, min(MATE_CP, cp))
    return round(50 + 50 * (2 / (1 + math.exp(-0.00368208 * cp)) - 1), 1)


def eval_to_cp(ev: Dict[str, Any]) -> float:
    """White-POV centipawns from an engine result, mate clamped to +-MATE_CP."""
    if ev.get("mate") is not None:
        return MATE_CP if ev["mate"] > 0 else -MATE_CP
    return max(-MATE_CP, min(MATE_CP, ev.get("cp") or 0))


def classify_quality(cp_loss: float, wp_drop: float, played_is_best: bool, is_book: bool) -> str:
    if is_book and cp_loss <= 50:
        return "Book"
    if played_is_best or cp_loss <= 10:
        return "Best"
    if wp_drop >= 15:
        return "Blunder"
    if wp_drop >= 10:
        return "Mistake"
    if wp_drop >= 5:
        return "Inaccuracy"
    return "Good"


# ---------------------------------------------------------------------------
# Opening
# ---------------------------------------------------------------------------
def opening_context(uci_from_start: Optional[List[str]]) -> Dict[str, Any]:
    """Opening name/ECO from the moves so far; is_book_move if this move is still inside a known line."""
    if not uci_from_start:
        return {"eco": None, "name": None, "is_book_move": False}
    best_name, best_eco, best_len = None, None, 0
    in_book = False
    for seq, entry in ECO_DATABASE.items():
        line = seq.split()
        if uci_from_start[:len(line)] == line and len(line) > best_len:
            best_name, best_eco, best_len = entry["name"], entry["eco"], len(line)
        if line[:len(uci_from_start)] == uci_from_start:
            in_book = True
        # One of the listed continuations of a known line also counts as book
        if uci_from_start[:-1] == line and any(c["move"] == uci_from_start[-1] for c in entry.get("continuations", [])):
            in_book = True
    return {"eco": best_eco, "name": best_name, "is_book_move": in_book}


# ---------------------------------------------------------------------------
# Per-move analysis
# ---------------------------------------------------------------------------
def analyze_move(
    fen_before: str,
    move_uci: str,
    move_number: int,
    eval_before: Optional[Dict[str, Any]],
    eval_after: Optional[Dict[str, Any]],
    uci_from_start: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    eval_before / eval_after: {"cp": int|None, "mate": int|None, "best_move": uci, "depth": int, "source": str}
    (White POV). Either may be None if no engine is available; engine fields are then null.
    """
    before = chess.Board(fen_before)
    move = chess.Move.from_uci(move_uci)
    if move not in before.legal_moves:
        raise ValueError(f"Illegal move {move_uci} in {fen_before}")
    mover = before.turn
    opp = not mover
    san = before.san(move)
    captured = before.piece_at(move.to_square) if not before.is_en_passant(move) else chess.Piece(chess.PAWN, opp)
    moved_piece = before.piece_at(move.from_square)
    after = before.copy(stack=False)
    after.push(move)

    phase = ChessTranslator.determine_game_phase(before, move_number)
    opening = opening_context(uci_from_start)
    context = {
        "phase": phase,
        "opening": opening,
        "move_number": move_number,
        "color": "w" if mover == chess.WHITE else "b",
        "move_san": san,
        "fen_before": fen_before,
        "fen_after": after.fen(),
    }

    # ---- engine block ----
    engine = None
    cp_loss = 0.0
    wp_drop = 0.0
    if eval_before and eval_after:
        sign = 1 if mover == chess.WHITE else -1
        cp_b, cp_a = eval_to_cp(eval_before), eval_to_cp(eval_after)
        best_uci = eval_before.get("best_move") or None
        played_is_best = best_uci == move_uci
        cp_loss = 0.0 if played_is_best else max(0.0, sign * (cp_b - cp_a))
        wp_b, wp_a = win_prob(cp_b, mover), win_prob(cp_a, mover)
        wp_drop = 0.0 if played_is_best else max(0.0, wp_b - wp_a)
        quality = classify_quality(cp_loss, wp_drop, played_is_best, opening["is_book_move"])
        mover_mate_before = eval_before.get("mate") is not None and sign * eval_before["mate"] > 0
        mover_mate_after = eval_after.get("mate") is not None and sign * eval_after["mate"] > 0
        lost_mate = mover_mate_before and not mover_mate_after and not after.is_checkmate()
        if lost_mate and quality in ("Best", "Good", "Book"):
            # Letting a forced mate slip: still winning means Inaccuracy, otherwise Mistake
            quality = "Inaccuracy" if sign * cp_a >= 500 else "Mistake"
        best_san = None
        if best_uci:
            try:
                best_san = before.san(chess.Move.from_uci(best_uci))
            except Exception:
                best_san = None
        engine = {
            "eval_before": None if eval_before.get("mate") is not None else round(cp_b / 100, 2),
            "eval_after": None if eval_after.get("mate") is not None else round(cp_a / 100, 2),
            "mate_before": eval_before.get("mate"),
            "mate_after": eval_after.get("mate"),
            "eval_delta": round(sign * (cp_a - cp_b) / 100, 2),  # mover POV, pawns
            "cp_loss": round(cp_loss),
            "win_prob_before": wp_b,  # mover's winning chances
            "win_prob_after": wp_a,
            "best_move_uci": best_uci,
            "best_move_san": best_san,
            "played_is_best": played_is_best,
            "quality": quality,
            "missed_opportunity": lost_mate or (sign * cp_b >= 200 and sign * cp_a < 100 and quality in ("Mistake", "Blunder")),
            "missed_mate": lost_mate,
            "depth": min(eval_before.get("depth") or 0, eval_after.get("depth") or 0) or None,
            "source": eval_before.get("source"),
        }

    # ---- motifs ----
    mine_before = detect_opportunities(before, mover)
    mine_after = detect_opportunities(after, mover)
    theirs_before = detect_opportunities(before, opp)
    theirs_after = detect_opportunities(after, opp)

    motifs_for = []
    for key, (mid, score, detail) in mine_after.items():
        if key not in mine_before:
            motifs_for.append({"id": mid, "score": score, "status": "created", "detail": detail})
    motifs_for.extend(dict(m, status="created") for m in _discovered_attacks(before, after, move, mover))
    opp_king = after.king(opp)
    opp_back = 0 if opp == chess.WHITE else 7
    if (moved_piece.piece_type in (chess.ROOK, chess.QUEEN) and after.is_check() and opp_king is not None
            and chess.square_rank(opp_king) == opp_back and chess.square_rank(move.to_square) == opp_back):
        if after.is_checkmate():
            motifs_for.append({"id": "back_rank", "score": 100, "status": "created", "detail": f"{san} is back-rank mate"})
        elif captured:
            motifs_for.append({"id": "back_rank", "score": _clamp(55 + 4 * VALUES[captured.piece_type]),
                               "status": "created", "detail": f"{san} captures with a back-rank check"})
        else:
            stuck = all(chess.square_rank(km.to_square) == opp_back for km in after.legal_moves if km.from_square == opp_king)
            if stuck:
                motifs_for.append({"id": "back_rank", "score": 45, "status": "created",
                                   "detail": f"{san} checks the king stuck on its back rank"})

    motifs_against = []
    for key, (mid, score, detail) in theirs_after.items():
        if key not in theirs_before:
            motifs_against.append({"id": mid, "score": score, "status": "allowed", "detail": detail})
        elif mid in IGNORABLE_THREATS:
            motifs_against.append({"id": mid, "score": _clamp(score * 0.8), "status": "ignored", "detail": detail})

    shield_lost = _king_shield(before, mover) - _king_shield(after, mover)
    king_sq = before.king(mover)
    king_tucked = king_sq is not None and chess.square_file(king_sq) in (0, 1, 2, 6, 7)  # castled / on a wing
    if shield_lost > 0 and king_tucked and phase != "endgame" and moved_piece.piece_type == chess.PAWN:
        motifs_against.append({"id": "exposed_king", "score": _clamp(30 + 10 * shield_lost), "status": "created",
                               "detail": f"{san} removes a pawn from the king's shield"})
    weak_added = _pawn_weakness_count(after, mover) - _pawn_weakness_count(before, mover)
    if weak_added > 0:
        motifs_against.append({"id": "pawn_weakness", "score": _clamp(20 * weak_added, 0, 60), "status": "created",
                               "detail": f"{san} creates doubled/isolated pawns"})
    if (engine and captured and captured.piece_type != chess.PAWN
            and (engine["eval_before"] or 0) * (1 if mover == chess.WHITE else -1) >= 1.5):
        motifs_for.append({"id": "simplification", "score": 25, "status": "created",
                           "detail": f"{san} trades down while ahead"})

    # Let the engine veto patterns that are not real: a "threat" the opponent cannot
    # exploit cost nothing, and a "tactic" in a losing move did not work.
    if engine:
        if cp_loss < 50:
            for m in motifs_against:
                if m["id"] in TACTICAL_MOTIFS:
                    m["score"] = _clamp(m["score"] * 0.4)
        elif cp_loss >= 150:
            for m in motifs_against:
                if m["id"] in TACTICAL_MOTIFS:
                    m["score"] = _clamp(m["score"] * 1.25)
        if cp_loss > 150:
            # Whatever the move "built" did not hold up: the engine says it lost material/position
            for m in motifs_for:
                m["score"] = _clamp(m["score"] * 0.5)

    motifs_for = _merge_motifs(motifs_for)
    motifs_against = _merge_motifs(motifs_against)

    primary = None
    candidates = [dict(m, side="for") for m in motifs_for] + [dict(m, side="against") for m in motifs_against]
    if candidates:
        top = max(candidates, key=lambda m: m["score"])
        primary = {"id": top["id"], "side": top["side"], "score": top["score"]}

    if opening["is_book_move"]:
        category = "book"
    elif any(m["id"] in TACTICAL_MOTIFS and m["score"] >= 50 for m in candidates):
        category = "tactical"
    elif candidates:
        category = "positional"
    else:
        category = "quiet"

    # ---- six aspects ----
    positional_for = sum(m["score"] for m in motifs_for if m["id"] not in TACTICAL_MOTIFS)
    mobility_gain = _mobility(after, mover) - _mobility(before, mover)
    development = 0
    if phase == "opening":
        home_rank = 0 if mover == chess.WHITE else 7
        if before.is_castling(move):
            development = 30
        elif moved_piece.piece_type in (chess.KNIGHT, chess.BISHOP) and chess.square_rank(move.from_square) == home_rank:
            development = 20
    building = _clamp(positional_for + 3 * mobility_gain + development)

    material_won = VALUES[captured.piece_type] * 10 if captured else 0
    if move.promotion:
        material_won += 80
    if after.is_checkmate():
        material_won = 100
    score_aspect = _clamp(material_won)

    tactical_for = max([m["score"] for m in motifs_for if m["id"] in TACTICAL_MOTIFS], default=0)
    seizing = tactical_for
    if engine and engine["played_is_best"] and material_won:
        seizing = max(seizing, score_aspect)
    seizing = _clamp(seizing)

    opp_mobility_cut = _mobility(before, opp) - _mobility(after, opp)
    dismantled = sum(score for key, (mid, score, _) in theirs_before.items() if key not in theirs_after)
    preventing = _clamp(3 * opp_mobility_cut + 0.5 * dismantled)

    worst_against = max([m["score"] for m in motifs_against if m["id"] in TACTICAL_MOTIFS], default=0)
    avoiding = _clamp(100 - max(worst_against, min(100, cp_loss / 3)))
    opponent_score = _clamp(2 * wp_drop) if engine else None
    if engine is None:
        # Without an engine we cannot tell real threats from harmless ones.
        avoiding = _clamp(100 - worst_against)

    aspects = {
        "building_state": building,
        "seizing_opportunity": seizing,
        "score": score_aspect,
        "preventing_opponent_building_state": preventing,
        "avoiding_opponent_seizing_opportunity": avoiding,
        "opponent_score": opponent_score,
    }

    return {
        "schema_version": 2,
        "context": context,
        "engine": engine,
        "move": {
            "aspects": aspects,
            "motifs_for": motifs_for,
            "motifs_against": motifs_against,
            "primary_motif": primary,
            "category": category,
            "is_check": after.is_check(),
            "is_capture": captured is not None,
        },
    }


# ---------------------------------------------------------------------------
# Per-sequence analysis (window of plies ending at the node)
# ---------------------------------------------------------------------------
ASPECT_KEYS = [
    "building_state", "seizing_opportunity", "score",
    "preventing_opponent_building_state", "avoiding_opponent_seizing_opportunity", "opponent_score",
]


def build_sequence_analysis(color: str, plies: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    color: the node mover ('w'/'b'). plies: oldest-first list ending with the node itself;
    each item is a node analysis dict (schema v2) with context/engine/move filled in.
    """
    mine = [p for p in plies if p["context"]["color"] == color]
    sign = 1 if color == "w" else -1

    def cp_of(eval_pawns, mate):
        if mate is not None:
            return MATE_CP if mate > 0 else -MATE_CP
        return (eval_pawns or 0) * 100

    first_eng, last_eng = plies[0].get("engine"), plies[-1].get("engine")
    eval_change = None
    trend = None
    if first_eng and last_eng:
        start = cp_of(first_eng["eval_before"], first_eng["mate_before"])
        end = cp_of(last_eng["eval_after"], last_eng["mate_after"])
        eval_change = round(sign * (end - start) / 100, 2)
        trend = "rising" if eval_change >= 0.5 else ("declining" if eval_change <= -0.5 else "steady")

    aspects = {}
    for k in ASPECT_KEYS:
        vals = [p["move"]["aspects"].get(k) for p in mine if p["move"]["aspects"].get(k) is not None]
        aspects[k] = round(sum(vals) / len(vals)) if vals else None

    errors = {"Inaccuracy": 0, "Mistake": 0, "Blunder": 0}
    for p in mine:
        q = (p.get("engine") or {}).get("quality")
        if q in errors:
            errors[q] += 1

    motifs_for, motifs_against = [], []
    for p in plies:
        own = p["context"]["color"] == color
        tag = f"{p['context']['move_number']}{'.' if p['context']['color'] == 'w' else '...'}{p['context']['move_san']}"
        for m in p["move"]["motifs_for"]:
            (motifs_for if own else motifs_against).append(dict(m, ply=tag))
        for m in p["move"]["motifs_against"]:
            (motifs_against if own else motifs_for).append(dict(m, ply=tag))

    return {
        "window_plies": len(plies),
        "moves": [p["context"]["move_san"] for p in plies],
        "eval_change": eval_change,
        "eval_trend": trend,
        "aspects": aspects,
        "errors": errors,
        "motifs_for": _merge_motifs(motifs_for),
        "motifs_against": _merge_motifs(motifs_against),
    }
