"""
Baby-Step Drill Generator for Chess Pedagogical Mastery.
Generates a structured 3-stage progression for any tactical motif or recurring error:
- Stage 1: Clean Board (Minimal pieces, raw geometric mechanic in pure isolation)
- Stage 2: Stepping Stone (Intermediate setup / preventative warning signs)
- Stage 3: Real Board Mastery (The full-game position or reciprocal challenge)
"""
from typing import Dict, Any, List, Optional
import chess

BABY_STEP_CURRICULUM = {
    "back_rank": {
        "title": "Corridor & Back-Rank Mastery",
        "concept": "A king boxed in by its own pawn shield on the 8th or 1st rank is vulnerable to a decisive heavy-piece invasion.",
        "stage1": {
            "title": "Stage 1: Raw Geometry (Pure Back-Rank Mate)",
            "description": "Notice how Black's three pawns (f7, g7, h7) block the king completely. White's rook delivers checkmate along the back rank with no escape.",
            "fen": "6k1/5ppp/8/8/8/8/8/4R1K1 w - - 0 1",
            "turn": "w",
            "goal": "Deliver checkmate in 1 move using the open file.",
            "best_move_san": "Re8#",
            "best_move_uci": "e1e8",
            "takeaway": "When your king has no 'luft' (escape air), any back-rank check is fatal."
        },
        "stage2": {
            "title": "Stage 2: Stepping Stone (Creating Luft / Prevention)",
            "description": "White has rooks doubled on the e-file and is threatening a back-rank mate. Black must create an escape hatch before the invasion occurs.",
            "fen": "4r1k1/5ppp/8/8/8/4R3/5PPP/4R1K1 b - - 0 1",
            "turn": "b",
            "goal": "Push a pawn to create luft and avoid back-rank catastrophe.",
            "best_move_san": "h6",
            "best_move_uci": "h7h6",
            "takeaway": "Creating luft (h3/h6) gives your king an escape square and completely disarms back-rank threats."
        }
    },
    "fork": {
        "title": "Double Attack & Knight Fork Mastery",
        "concept": "A single piece simultaneously attacks two or more enemy pieces, forcing the opponent to lose material.",
        "stage1": {
            "title": "Stage 1: Raw Geometry (The Classic Royal Fork)",
            "description": "Knights move in an 'L' shape (2 squares in one direction, 1 square perpendicular). From d5, leap the knight to f6 (1. Nf6+), simultaneously checking the King on e8 and attacking the Queen on d7!",
            "fen": "4k3/3q4/8/3N4/8/8/8/4K3 w - - 0 1",
            "turn": "w",
            "goal": "Leap the knight to f6 (1. Nf6+) to deliver the royal fork.",
            "best_move_san": "Nf6+",
            "best_move_uci": "d5f6",
            "sequence": ["d5f6", "e8e7", "f6d7"],
            "takeaway": "Knights excel at forking pieces that are on squares of the same color."
        },
        "stage2": {
            "title": "Stage 2: Stepping Stone (The Open-File Deflection Fork - ~1300 ELO)",
            "description": "A realistic middlegame position. Black's queen on d8 and corner rook on a8 are vulnerable to a fork on c7, but the e-file is guarded. Deflect Black's queen by exchanging rooks with 1. Rxe8+! When Black recaptures (1... Qxe8), deliver the deadly fork with 2. Nc7!",
            "fen": "r2qr1k1/ppp2ppp/5n2/3N4/8/5Q2/PPP2PPP/3RR1K1 w - - 0 1",
            "turn": "w",
            "goal": "Trade rooks on e8 (1. Rxe8+), then fork the Queen and corner Rook (2. Nc7).",
            "best_move_san": "Rxe8+",
            "best_move_uci": "e1e8",
            "sequence": ["e1e8", "d8e8", "d5c7", "e8e7", "c7a8"],
            "takeaway": "Forcing exchanges can pull high-value pieces onto geometric fork squares."
        },
        "stage3": {
            "title": "Stage 3: Full Combat Mastery (Removing the Guard - ~1600 ELO)",
            "description": "Full piece combat. Black's Queen on d7 and King on g8 are perfectly aligned for a royal fork on f6, but Black's knight on f6 guards the square! Eliminate the defender with 1. Bxf6! When Black recaptures (1... Bxf6), unleash the devastating royal fork with 2. Nxf6+!",
            "fen": "4r1k1/pp1q1pbp/2p2np1/3N2B1/8/2P5/PP3PPP/R2QR1K1 w - - 0 1",
            "turn": "w",
            "goal": "Remove the defender with 1. Bxf6, then deliver the 2. Nxf6+ royal fork to win the Queen.",
            "best_move_san": "Bxf6",
            "best_move_uci": "g5f6",
            "sequence": ["g5f6", "g7f6", "d5f6", "g8g7", "f6d7"],
            "takeaway": "When an opponent piece guards a fatal fork square, eliminating the guard unlocks decisive tactical wins."
        }
    },
    "pin": {
        "title": "Absolute & Relative Pin Mastery",
        "concept": "A piece cannot move (or cannot safely move) because doing so exposes a more valuable piece behind it.",
        "stage1": {
            "title": "Stage 1: Raw Geometry (Piling On the Pinned Piece)",
            "description": "Black's knight on d7 is pinned to the King on e8 by White's bishop on b5. Pinned pieces cannot move, making them ideal targets to attack with pawns.",
            "fen": "4k3/3n4/8/1B6/3P4/8/8/4K3 w - - 0 1",
            "turn": "w",
            "goal": "Push the pawn to attack and win the paralyzed knight.",
            "best_move_san": "d5",
            "best_move_uci": "d4d5",
            "takeaway": "The golden rule of pins: always pile pressure onto the pinned piece, especially with pawns!"
        },
        "stage2": {
            "title": "Stage 2: Stepping Stone (Neutralizing the Pin)",
            "description": "White's bishop on g5 pins Black's knight on f6 to the queen. Black should break the pin by developing the bishop to e7.",
            "fen": "r1bqkb1r/ppp2ppp/2np1n2/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R b KQkq - 1 5",
            "turn": "b",
            "goal": "Neutralize the pin by developing your dark-squared bishop to e7.",
            "best_move_san": "Be7",
            "best_move_uci": "f8e7",
            "takeaway": "Interposing a piece or breaking the pin early prevents opponent tactics."
        }
    },
    "skewer": {
        "title": "Skewer / X-Ray Mastery",
        "concept": "A valuable piece is attacked in front, forcing it to move and exposing a vulnerable piece lined up behind it.",
        "stage1": {
            "title": "Stage 1: Raw Geometry (The Heavy-Piece Skewer)",
            "description": "Black's King is on e8, directly in front of the Rook on e2. White's Rook can check along the e-file, piercing through to the rook behind.",
            "fen": "4k3/8/8/8/8/8/4r3/4R1K1 w - - 0 1",
            "turn": "w",
            "goal": "Check the king and skewer the rook on the e-file.",
            "best_move_san": "Rxe2+",
            "best_move_uci": "e1e2",
            "takeaway": "Never place high-value pieces in front of lesser-defended pieces on open ranks or files."
        },
        "stage2": {
            "title": "Stage 2: Stepping Stone (Avoiding the Skewer Alignment)",
            "description": "White threatens Bf4+ skewering Black's King on e5 and Queen on c7. Step the king off the fatal line immediately.",
            "fen": "8/2q5/8/4k3/8/4B3/5P2/4K3 b - - 0 1",
            "turn": "b",
            "goal": "Move the king off the diagonal to prevent the Bf4+ bishop skewer.",
            "best_move_san": "Kd6",
            "best_move_uci": "e5d6",
            "takeaway": "Stepping off open diagonals before opponent bishops align prevents deadly skewers."
        }
    },
    "hanging_piece": {
        "title": "Loose Pieces & Undefended Targets Mastery",
        "concept": "'Loose pieces drop off' (LPDO). An undefended piece is a magnet for tactical combinations.",
        "stage1": {
            "title": "Stage 1: Raw Geometry (Spotting the Free Target - ~800 ELO)",
            "description": "Black's bishop on a8 has zero defenders. Because the entire a-file is wide open, White's queen on a1 can capture it directly with 1. Qxa8+.",
            "fen": "b3k3/8/8/8/8/8/8/Q3K3 w - - 0 1",
            "turn": "w",
            "goal": "Capture the undefended bishop on a8 in one move (1. Qxa8+).",
            "best_move_san": "Qxa8+",
            "best_move_uci": "a1a8",
            "sequence": ["a1a8"],
            "takeaway": "Every move, scan the board for opponent pieces that have 0 defenders."
        },
        "stage2": {
            "title": "Stage 2: Stepping Stone (The Qa4+ Fork on the Loose Bishop - ~1300 ELO)",
            "description": "Black developed their dark-squared bishop to b4 without protecting it. White can punish this loose piece with the classic 1. Qa4+ check, simultaneously checking the King on e8 and attacking the undefended bishop on b4! After Black blocks with 1... Bd7, snap up the free bishop with 2. Qxb4!",
            "fen": "r1bqk1nr/ppp2ppp/4p3/3p4/1bPP4/2N1P3/PP3PPP/R1BQKBNR w KQkq - 0 5",
            "turn": "w",
            "goal": "Deliver check with 1. Qa4+ to double-attack the King and loose Bishop on b4, then capture it.",
            "best_move_san": "Qa4+",
            "best_move_uci": "d1a4",
            "sequence": ["d1a4", "c8d7", "a4b4"],
            "takeaway": "Loose pieces drop off! Whenever an enemy piece moves without defense, look for double attacks and checks."
        },
        "stage3": {
            "title": "Stage 3: Full Combat Mastery (Deflecting the Defender - ~1600 ELO)",
            "description": "Full middlegame tactical combination. Black's knight on a5 sits loosely on the rim, defended ONLY by Black's Queen on e7. White deflects the Queen by exchanging rooks on d8: 1. Rxd8+! When Black is forced to recapture with the Queen (1... Qxd8), Black's knight on a5 is left completely undefended: 2. Qxa5 wins the piece!",
            "fen": "3r2k1/pp2qppp/4b3/n7/Q1B5/8/PP3PPP/3R2K1 w - - 0 1",
            "turn": "w",
            "goal": "Deflect the Queen with 1. Rxd8+ Qxd8, then capture the undefended knight with 2. Qxa5.",
            "best_move_san": "Rxd8+",
            "best_move_uci": "d1d8",
            "sequence": ["d1d8", "e7d8", "a4a5"],
            "takeaway": "When an enemy piece has only a single defender, deflecting or removing that defender wins the loose target."
        }
    },
    "trapped_piece": {
        "title": "Trapped Piece & Restricted Mobility Mastery",
        "concept": "A piece with no safe escape squares can be surrounded and captured even if it is not immediately attacked.",
        "stage1": {
            "title": "Stage 1: Raw Geometry (Enclosing the Knight)",
            "description": "Black's knight on a1 is stuck on the corner with zero safe flight squares. White's king can step up to trap and win it.",
            "fen": "4k3/8/8/8/8/8/4P3/n3K3 w - - 0 1",
            "turn": "w",
            "goal": "Step the King up to trap the cornered knight (Kd2).",
            "best_move_san": "Kd2",
            "best_move_uci": "e1d2",
            "takeaway": "Knights on the rim or in corner pockets quickly run out of squares."
        },
        "stage2": {
            "title": "Stage 2: Stepping Stone (Securing Escape Squares)",
            "description": "Before pushing pawns forward, ensure your minor pieces retain safe retreat squares.",
            "fen": "r1bqk2r/pppp1ppp/2n5/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R b KQkq - 0 4",
            "turn": "b",
            "goal": "Solidify the center and create retreat paths for your pieces.",
            "best_move_san": "d6",
            "best_move_uci": "d7d6",
            "takeaway": "Always monitor your pieces' retreat routes before the position closes up."
        }
    },
    "battery": {
        "title": "Battery & Aligned Heavy Pieces Mastery",
        "concept": "Doubling heavy pieces (Queen + Rook or Rook + Rook) on a file concentrates irresistible pressure on key entry points.",
        "stage1": {
            "title": "Stage 1: Raw Geometry (Heavy Battery Infiltration)",
            "description": "White has doubled heavy pieces on the e-file (Queen on e2 backed by Rook on e1). Strike through Black's blocked rook with checkmate.",
            "fen": "4k3/4r3/8/8/8/8/4Q3/4R1K1 w - - 0 1",
            "turn": "w",
            "goal": "Deliver checkmate along the e-file using your doubled battery (Qxe7#).",
            "best_move_san": "Qxe7#",
            "best_move_uci": "e2e7",
            "takeaway": "A battery multiplies attacking power along open files and diagonals."
        },
        "stage2": {
            "title": "Stage 2: Stepping Stone (Preparing Harmony)",
            "description": "Connect your heavy pieces and prepare rooks for open files.",
            "fen": "r1bqk2r/pppp1ppp/2n5/4p3/4P3/2NP1N2/PPP2PPP/R2QKB1R w KQkq - 0 5",
            "turn": "w",
            "goal": "Develop the bishop to connect your back-rank rooks.",
            "best_move_san": "Be2",
            "best_move_uci": "f1e2",
            "takeaway": "Completing development enables your rooks to coordinate and double."
        }
    },
    "overloaded_defender": {
        "title": "Overloaded Defender & Deflection Mastery",
        "concept": "When an enemy piece is tasked with defending multiple critical points, attacking one deflects it from the other.",
        "stage1": {
            "title": "Stage 1: Raw Geometry (Punishing the Overworked Piece)",
            "description": "Black's rook on d8 cannot protect the Queen on d7 without abandoning defense. White's rook wins the Queen directly.",
            "fen": "3r2k1/3q4/8/8/8/8/8/3R2K1 w - - 0 1",
            "turn": "w",
            "goal": "Capture Black's queen with your rook (Rxd7).",
            "best_move_san": "Rxd7",
            "best_move_uci": "d1d7",
            "takeaway": "Look for enemy pieces carrying too many defensive jobs at once."
        },
        "stage2": {
            "title": "Stage 2: Stepping Stone (Reinforcing Overworked Pieces)",
            "description": "Support your center so single pieces don't become overloaded under enemy pressure.",
            "fen": "r2q1rk1/ppp2ppp/2n5/4p3/4P3/3P1N2/PPP2PPP/R2Q1RK1 w - - 0 9",
            "turn": "w",
            "goal": "Solidify the pawn structure and relieve tension.",
            "best_move_san": "c3",
            "best_move_uci": "c2c3",
            "takeaway": "Proactively assign secondary defenders to key squares."
        }
    },
    "discovered_attack": {
        "title": "Discovered Attack & Check Mastery",
        "concept": "Moving one piece unmasks a hidden line of attack from another piece, creating dual simultaneous threats.",
        "stage1": {
            "title": "Stage 1: Raw Geometry (Unmasking the Battery)",
            "description": "White's rook on d1 is aimed at Black's queen on d8, masked only by White's knight on d4. Moving the knight with check unleashes the rook.",
            "fen": "3q4/4k3/8/8/3N4/8/8/3R1K2 w - - 0 1",
            "turn": "w",
            "goal": "Jump the knight with check to win Black's queen by discovered attack.",
            "best_move_san": "Nc6+",
            "best_move_uci": "d4c6",
            "takeaway": "Discovered checks are devastating because the moving piece can attack anything while the opponent must answer check."
        },
        "stage2": {
            "title": "Stage 2: Stepping Stone (Breaking the X-Ray Line)",
            "description": "Black's king or queen is aligned with White's rook. Move off the line before the ambush springs.",
            "fen": "r1bqk2r/ppppbppp/2n5/4p3/4P3/3P1N2/PPP2PPP/RNBQ1RK1 b kq - 0 5",
            "turn": "b",
            "goal": "Castle your king to safety away from the center line.",
            "best_move_san": "O-O",
            "best_move_uci": "e8g8",
            "takeaway": "Never allow your king to stay on the same file as an enemy rook, even with pieces in between."
        }
    }
}


async def generate_baby_step_progression(
    motif_id: str,
    root_fen: Optional[str] = None,
    move_san: Optional[str] = None,
    best_move_san: Optional[str] = None,
    best_move_uci: Optional[str] = None,
    player_color: str = "w",
    game_title: Optional[str] = None,
    engine_manager: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Constructs a 3-stage progressive drill.
    If root_fen and best_move_san are provided (a specific blunder from a game):
      - Stage 1: Fix Your Blunder (find the master move from root_fen).
      - Stage 2: Punish the Blunder (step into opponent's shoes to play the refutation move).
      - Stage 3: Full Combat Mastery (prove complete control from the game position).
    If root_fen is omitted (generic motif practice):
      - Stage 1: Clean board raw geometry.
      - Stage 2: Intermediate setup warning signs.
      - Stage 3: Reciprocal challenge.
    """
    # Normalize motif id
    clean_id = (motif_id or "hanging_piece").lower().replace(" ", "_")
    if clean_id not in BABY_STEP_CURRICULUM:
        for k in BABY_STEP_CURRICULUM:
            if k in clean_id or clean_id in k:
                clean_id = k
                break
    
    curriculum = BABY_STEP_CURRICULUM.get(clean_id, BABY_STEP_CURRICULUM["back_rank"])

    # Check if this is a game-specific blunder position
    board_before = None
    if root_fen:
        try:
            b_cand = chess.Board(root_fen)
            if b_cand.is_valid():
                board_before = b_cand
        except Exception:
            board_before = None

    if board_before and (best_move_san or move_san):
        # Resolve best move if missing
        if not best_move_san and engine_manager:
            try:
                res = await engine_manager.evaluate_position(board_before, depth=10)
                best_move_san = res.get("best_move_san")
                best_move_uci = res.get("best_move")
            except Exception:
                pass

        turn_color = "w" if board_before.turn == chess.WHITE else "b"

        # Stage 1: Fix Your Blunder (Find the Master Move)
        s1 = {
            "step": 1,
            "difficulty": "Baby Step 1: Fix Your Blunder (Direct Defense)",
            "title": f"Stage 1: Find the Master Move ({best_move_san or 'Best Move'})",
            "description": f"In {game_title or 'your game'}, {move_san or 'a blunder'} was played. Spot the master move ({best_move_san or 'optimal move'}) to secure your position!",
            "fen": root_fen,
            "turn": turn_color,
            "goal": f"Play the optimal move ({best_move_san or 'best move'}) from this position.",
            "best_move_san": best_move_san or "Best move",
            "best_move_uci": best_move_uci or "",
            "takeaway": "Spotting the defensive or tactical alternative under real pressure prevents critical material loss."
        }

        # Stage 2: Punish the Blunder (Play as Opponent)
        s2 = None
        if move_san:
            try:
                b_after = board_before.copy()
                clean_san = move_san.rstrip("?!+#")
                m_blunder = None
                for cand in [clean_san, move_san]:
                    try:
                        m_blunder = b_after.parse_san(cand)
                        break
                    except Exception:
                        pass
                if m_blunder and m_blunder in b_after.legal_moves:
                    b_after.push(m_blunder)
                    fen_after = b_after.fen()
                    opp_color = "w" if b_after.turn == chess.WHITE else "b"
                    opp_best_san = "the refutation"
                    opp_best_uci = ""
                    if engine_manager:
                        try:
                            eval_res = await engine_manager.evaluate_position(b_after, depth=10)
                            opp_best_san = eval_res.get("best_move_san") or "the refutation"
                            opp_best_uci = eval_res.get("best_move") or ""
                        except Exception:
                            pass
                    s2 = {
                        "step": 2,
                        "difficulty": "Baby Step 2: Step Into Opponent's Shoes (The Refutation)",
                        "title": f"Stage 2: Punish the Blunder ({move_san})",
                        "description": f"Understand why {move_san} failed! Step into your opponent's shoes and find the refutation ({opp_best_san}) that exploits the mistake.",
                        "fen": fen_after,
                        "turn": opp_color,
                        "goal": f"Find the opponent's strongest reply punishing {move_san} ({opp_best_san}).",
                        "best_move_san": opp_best_san,
                        "best_move_uci": opp_best_uci,
                        "takeaway": "Seeing how opponents punish our moves builds bulletproof tactical awareness."
                    }
            except Exception:
                s2 = None

        if not s2:
            s2 = dict(curriculum["stage2"])
            s2["step"] = 2
            s2["difficulty"] = "Baby Step 2: Stepping Stone (Warning Signs & Prevention)"

        # Stage 3: Full Combat Mastery
        s3 = {
            "step": 3,
            "difficulty": "Baby Step 3: Full Combat Mastery (Your Game)",
            "title": f"Stage 3: Complete Position Mastery ({game_title or 'Your Game'})",
            "description": f"Return to your critical position. Play {best_move_san or 'the master move'} and fight out the resulting lines against Stockfish to prove full mastery!",
            "fen": root_fen,
            "turn": turn_color,
            "goal": f"Play {best_move_san or 'the best move'} and continue the game to victory!",
            "best_move_san": best_move_san or "Best move",
            "best_move_uci": best_move_uci or "",
            "takeaway": "Consistent pattern recognition turns former mistakes into permanent competitive advantages."
        }

        return {
            "success": True,
            "motif_id": clean_id,
            "title": f"Game Mastery: {game_title or 'Blunder Recovery'}",
            "concept": f"Targeted 3-step workout addressing {move_san or 'the blunder'} with master move {best_move_san or 'best move'}.",
            "stages": [s1, s2, s3]
        }

    # Fallback to general pedagogical curriculum if no valid game position was supplied
    import backend.drill_bank as drill_bank

    bank_l1 = drill_bank.get_expanded_level_bank(clean_id, 1)
    bank_l2 = drill_bank.get_expanded_level_bank(clean_id, 2)
    bank_l3 = drill_bank.get_expanded_level_bank(clean_id, 3)

    s1 = dict(bank_l1[0])
    s1["step"] = 1
    s1["difficulty"] = "Level 1: Foundations (~800 ELO)"
    s1["riddles"] = bank_l1
    s1["riddle_index"] = 0
    s1["total_riddles"] = len(bank_l1)

    s2 = dict(bank_l2[0])
    s2["step"] = 2
    s2["difficulty"] = "Level 2: Stepping Stone (~1300 ELO)"
    s2["riddles"] = bank_l2
    s2["riddle_index"] = 0
    s2["total_riddles"] = len(bank_l2)

    s3 = dict(bank_l3[0])
    s3["step"] = 3
    s3["difficulty"] = "Level 3: Full Combat Mastery (~1600 ELO)"
    s3["riddles"] = bank_l3
    s3["riddle_index"] = 0
    s3["total_riddles"] = len(bank_l3)

    return {
        "success": True,
        "motif_id": clean_id,
        "title": curriculum["title"],
        "concept": curriculum["concept"],
        "stages": [s1, s2, s3]
    }
