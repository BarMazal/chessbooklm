"""
Classification Visualizer Engine:
Computes rich geometric board overlays, arrows, and multi-step forced refutation chains
for any analyzed move (Quality, Tactical Motifs, Blunders, Missed Opportunities).
"""

import chess
from typing import Dict, List, Any, Optional

VALUES = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 100}

def compute_move_classification_visualization(
    fen_before: Optional[str],
    fen_after: str,
    move_uci: str,
    best_move_uci: Optional[str] = None,
    quality: Optional[str] = None,
    primary_motif: Optional[Dict[str, Any]] = None,
    motifs_against: Optional[List[Dict[str, Any]]] = None,
    motifs_for: Optional[List[Dict[str, Any]]] = None,
    pv_moves: Optional[List[str]] = None
) -> Dict[str, Any]:
    b_after = chess.Board(fen_after)
    
    # Reconstruct b_before if missing
    b_before = None
    if fen_before:
        try:
            b_before = chess.Board(fen_before)
        except Exception:
            b_before = None
    if not b_before:
        # Step backwards if possible
        try:
            test_b = chess.Board(fen_after)
            test_b.pop()
            b_before = test_b
        except Exception:
            b_before = chess.Board(fen_after)

    mover = b_before.turn
    opp = not mover

    highlights: List[Dict[str, Any]] = []
    arrows: List[Dict[str, Any]] = []
    motifs_detected: List[Dict[str, Any]] = []

    # 1. Move Played Arrow & Highlight
    is_bad = quality in ["Blunder", "Mistake", "Inaccuracy"]
    if move_uci and len(move_uci) >= 4:
        from_sq = move_uci[:2]
        to_sq = move_uci[2:4]
        arrow_color = "#ef4444" if quality == "Blunder" else ("#f97316" if quality == "Mistake" else "#eab308" if is_bad else "#3b82f6")
        badge = "Blunder" if quality == "Blunder" else ("Mistake" if quality == "Mistake" else ("Inaccuracy" if quality == "Inaccuracy" else "Played"))
        arrows.append({
            "from": from_sq,
            "to": to_sq,
            "color": arrow_color,
            "style": "solid",
            "width": 6,
            "label": f"Played ({badge})",
            "category": "played"
        })
        highlights.append({
            "square": to_sq,
            "color": arrow_color,
            "type": "move_played",
            "badge": "❌" if is_bad else "✓"
        })

    # 2. Recommended Best Move Arrow & Highlight
    if best_move_uci and len(best_move_uci) >= 4 and best_move_uci != move_uci:
        b_from = best_move_uci[:2]
        b_to = best_move_uci[2:4]
        arrows.append({
            "from": b_from,
            "to": b_to,
            "color": "#10b981",
            "style": "solid",
            "width": 7,
            "label": "Best Move",
            "category": "best"
        })
        highlights.append({
            "square": b_to,
            "color": "#10b981",
            "type": "best_move",
            "badge": "⭐"
        })

    # 3. Detect Undefended / Hanging Pieces
    # Check friendly pieces left hanging or newly hanging on b_after
    for sq, p in b_after.piece_map().items():
        if p.color == mover and p.piece_type != chess.KING:
            opp_attackers = list(b_after.attackers(opp, sq))
            defenders = list(b_after.attackers(mover, sq))
            p_val = VALUES.get(p.piece_type, 1)

            is_hanging = False
            gain = 0
            if opp_attackers:
                if not defenders:
                    is_hanging = True
                    gain = p_val
                else:
                    cheapest_att = min(VALUES.get(b_after.piece_at(a).piece_type, 100) for a in opp_attackers)
                    if p_val > cheapest_att:
                        is_hanging = True
                        gain = p_val - cheapest_att

            if is_hanging:
                sq_name = chess.square_name(sq)
                highlights.append({
                    "square": sq_name,
                    "color": "#ef4444",
                    "type": "hanging_piece",
                    "badge": f"Undefended (+{gain})",
                    "pulse": True
                })
                motifs_detected.append({
                    "id": "hanging_piece",
                    "title": f"Undefended {p.symbol().upper()}{sq_name}",
                    "detail": f"{p.symbol().upper()} on {sq_name} is undefended and can be won (+{gain})."
                })
                for att in opp_attackers:
                    arrows.append({
                        "from": chess.square_name(att),
                        "to": sq_name,
                        "color": "#dc2626",
                        "style": "dashed",
                        "width": 4,
                        "label": "Attacks Loose Piece",
                        "category": "threat"
                    })

    # 4. Detect Missed Fork or Allowed Fork
    # A) Missed Fork via best_move_uci from b_before
    if best_move_uci and len(best_move_uci) >= 4:
        try:
            m_best = chess.Move.from_uci(best_move_uci)
            if m_best in b_before.legal_moves:
                test_b = b_before.copy()
                test_b.push(m_best)
                f_sq = m_best.to_square
                f_piece = test_b.piece_at(f_sq)
                if f_piece:
                    targets = []
                    for t in test_b.attacks(f_sq):
                        tp = test_b.piece_at(t)
                        if tp and tp.color == opp:
                            if tp.piece_type == chess.KING or not test_b.attackers(opp, t) or f_piece.piece_type in [chess.PAWN, chess.KNIGHT]:
                                targets.append(t)
                    if len(targets) >= 2:
                        f_name = chess.square_name(f_sq)
                        target_names = [chess.square_name(t) for t in targets]
                        motifs_detected.append({
                            "id": "fork",
                            "title": f"Missed Fork with {f_piece.symbol().upper()}{f_name}",
                            "detail": f"Playing {best_move_uci} forks {', '.join(target_names)}."
                        })
                        for t in targets:
                            t_name = chess.square_name(t)
                            arrows.append({
                                "from": f_name,
                                "to": t_name,
                                "color": "#f59e0b",
                                "style": "solid",
                                "width": 5,
                                "label": "Fork Target",
                                "category": "fork"
                            })
                            highlights.append({
                                "square": t_name,
                                "color": "#f59e0b",
                                "type": "fork_target",
                                "badge": "🎯 Fork Target"
                            })
        except Exception:
            pass

    # B) Allowed / Created Opponent Fork on b_after
    for sq, p in b_after.piece_map().items():
        if p.color == opp:
            targets = []
            for t in b_after.attacks(sq):
                tp = b_after.piece_at(t)
                if tp and tp.color == mover:
                    if tp.piece_type == chess.KING or not b_after.attackers(mover, t) or p.piece_type in [chess.PAWN, chess.KNIGHT]:
                        targets.append(t)
            if len(targets) >= 2:
                f_name = chess.square_name(sq)
                target_names = [chess.square_name(t) for t in targets]
                motifs_detected.append({
                    "id": "fork",
                    "title": f"Opponent Fork Threat ({p.symbol().upper()}{f_name})",
                    "detail": f"Opponent threatens fork against {', '.join(target_names)}."
                })
                for t in targets:
                    t_name = chess.square_name(t)
                    arrows.append({
                        "from": f_name,
                        "to": t_name,
                        "color": "#ea580c",
                        "style": "dashed",
                        "width": 5,
                        "label": "Threatened Fork",
                        "category": "threat"
                    })
                    highlights.append({
                        "square": t_name,
                        "color": "#ea580c",
                        "type": "threatened_target",
                        "badge": "⚠️ Fork Target"
                    })

    # 5. Detect Pins on b_after
    enemy_king = b_after.king(mover)
    for sq, p in b_after.piece_map().items():
        if p.color == opp and p.piece_type in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
            for t in b_after.attacks(sq):
                tp = b_after.piece_at(t)
                if tp and tp.color == mover:
                    # Check ray beyond
                    df = chess.square_file(t) - chess.square_file(sq)
                    dr = chess.square_rank(t) - chess.square_rank(sq)
                    if df == 0 or dr == 0 or abs(df) == abs(dr):
                        sf = (df > 0) - (df < 0)
                        sr = (dr > 0) - (dr < 0)
                        f, r = chess.square_file(t) + sf, chess.square_rank(t) + sr
                        behind_sq = None
                        while 0 <= f <= 7 and 0 <= r <= 7:
                            s_cand = chess.square(f, r)
                            if b_after.piece_at(s_cand):
                                behind_sq = s_cand
                                break
                            f += sf
                            r += sr
                        if behind_sq is not None:
                            behind = b_after.piece_at(behind_sq)
                            if behind and behind.color == mover:
                                if behind_sq == enemy_king or VALUES.get(behind.piece_type, 0) > VALUES.get(tp.piece_type, 0):
                                    t_name = chess.square_name(t)
                                    p_name = chess.square_name(sq)
                                    b_name = chess.square_name(behind_sq)
                                    highlights.append({
                                        "square": t_name,
                                        "color": "#a855f7",
                                        "type": "pinned_piece",
                                        "badge": "📌 Pinned"
                                    })
                                    arrows.append({
                                        "from": p_name,
                                        "to": b_name,
                                        "color": "#a855f7",
                                        "style": "dashed",
                                        "width": 4,
                                        "label": f"Pin along ray ({t_name} pinned to {b_name})",
                                        "category": "pin"
                                    })
                                    motifs_detected.append({
                                        "id": "pin",
                                        "title": f"Pinned Piece ({tp.symbol().upper()}{t_name})",
                                        "detail": f"{tp.symbol().upper()} on {t_name} is pinned to {behind.symbol().upper()} on {b_name} by {p.symbol().upper()} on {p_name}."
                                    })

    # 6. Detect Back Rank Vulnerability
    opp_king_sq = b_after.king(mover)
    back_rank_idx = 0 if mover == chess.WHITE else 7
    if opp_king_sq is not None and chess.square_rank(opp_king_sq) == back_rank_idx:
        # Check if king is boxed in
        king_moves = [m for m in b_after.legal_moves if m.from_square == opp_king_sq]
        is_boxed = all(chess.square_rank(m.to_square) == back_rank_idx for m in king_moves)
        if is_boxed and len(king_moves) <= 2:
            k_name = chess.square_name(opp_king_sq)
            highlights.append({
                "square": k_name,
                "color": "#e11d48",
                "type": "back_rank",
                "badge": "🏰 Back Rank Boxed In"
            })
            motifs_detected.append({
                "id": "back_rank",
                "title": "Back-Rank Weakness",
                "detail": f"King on {k_name} is boxed in on the back rank with no escape square."
            })

    # Ingest mentor / engine primary_motif and motifs_against if not already covered
    if primary_motif and isinstance(primary_motif, dict):
        pm_id = primary_motif.get("id")
        if pm_id and not any(m.get("id") == pm_id for m in motifs_detected):
            motifs_detected.append({
                "id": pm_id,
                "title": f"{pm_id.replace('_', ' ').title()}",
                "detail": primary_motif.get("detail") or f"Stockfish classified this move with {pm_id.replace('_', ' ')}."
            })
    if motifs_against and isinstance(motifs_against, list):
        for ma in motifs_against:
            if isinstance(ma, dict):
                ma_id = ma.get("id")
                if ma_id and not any(m.get("id") == ma_id for m in motifs_detected):
                    motifs_detected.append({
                        "id": ma_id,
                        "title": f"Threat: {ma_id.replace('_', ' ').title()}",
                        "detail": ma.get("detail") or f"Opponent creates {ma_id.replace('_', ' ')}."
                    })

    # 7. Multi-step Forced Refutation / Best Continuation Line
    forced_chain: List[Dict[str, Any]] = []
    if pv_moves:
        curr_b = b_after.copy()
        for idx, uci in enumerate(pv_moves[:5]):
            try:
                mv = chess.Move.from_uci(uci)
                if mv in curr_b.legal_moves:
                    san = curr_b.san(mv)
                    turn_char = "w" if curr_b.turn == chess.WHITE else "b"
                    curr_b.push(mv)
                    forced_chain.append({
                        "ply": idx + 1,
                        "uci": uci,
                        "san": san,
                        "color": turn_char,
                        "fen_after": curr_b.fen()
                    })
            except Exception:
                break

    return {
        "success": True,
        "fen_before": fen_before or b_before.fen(),
        "fen_after": fen_after,
        "move_uci": move_uci,
        "best_move_uci": best_move_uci,
        "quality": quality,
        "highlights": highlights,
        "arrows": arrows,
        "motifs": motifs_detected,
        "forced_chain": forced_chain
    }
