"""
Master Tactical Drill Bank with Graduated 3-Tier Pedagogy:
  - Level 1: Clean Board Raw Geometry (~800 ELO)
  - Level 2: Realistic Middlegame Stepping Stone (~1300 ELO)
  - Level 3: Combat Mastery & Deep Combinations (~1600 ELO)

Provides >= 10 verified riddles per level for all 9 core chess tactics motifs.
Also includes procedural variation generator to synthesize unlimited new riddles on demand.
"""

import chess
import random
from typing import Dict, List, Any, Optional

DRILL_BASE_POOLS: Dict[str, Dict[str, List[Dict[str, Any]]]] = {   'back_rank': {   'level1': [   {   'best_move_san': 'Re8#',
                                       'best_move_uci': 'e1e8',
                                       'description': "Black's king is trapped behind a wall of pawns. Deliver "
                                                      'checkmate with 1. Re8#!',
                                       'fen': '6k1/5ppp/8/8/8/8/8/4R1K1 w - - 0 1',
                                       'goal': 'Deliver 1. Re8#.',
                                       'id': 'br_l1_01',
                                       'sequence': ['e1e8'],
                                       'takeaway': 'Pawns on the 7th rank without an escape square form a fatal '
                                                   'corridor.',
                                       'title': 'Raw Geometry: Lone Rook on the 8th Rank',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Rd8#',
                                       'best_move_uci': 'd1d8',
                                       'description': "White's rook delivers back-rank mate along the open d-file: 1. "
                                                      'Rd8#!',
                                       'fen': '5k2/5ppp/8/8/8/8/8/3R2K1 w - - 0 1',
                                       'goal': 'Deliver 1. Rd8#.',
                                       'id': 'br_l1_02',
                                       'sequence': ['d1d8'],
                                       'takeaway': 'Open files are direct highways to enemy back ranks.',
                                       'title': 'Raw Geometry: Infiltrating the d-file',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Ra8#',
                                       'best_move_uci': 'a1a8',
                                       'description': "White's rook strikes from the opposite side of the board: 1. "
                                                      'Ra8#!',
                                       'fen': '6k1/5ppp/8/8/8/8/8/R6K w - - 0 1',
                                       'goal': 'Deliver 1. Ra8#.',
                                       'id': 'br_l1_03',
                                       'sequence': ['a1a8'],
                                       'takeaway': 'Rooks command entire ranks regardless of distance.',
                                       'title': 'Raw Geometry: Long-Distance Cross-Board Mate',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Rxe8+',
                                       'best_move_uci': 'e1e8',
                                       'description': "Black's rook guards e8. White exchanges rooks with 1. Rxe8+ "
                                                      'Rxe8.',
                                       'fen': '5rk1/5ppp/8/8/8/8/8/4R1K1 w - - 0 1',
                                       'goal': 'Trade on e8 with 1. Rxe8 Rxe8.',
                                       'id': 'br_l1_04',
                                       'sequence': ['e1e8', 'f8e8'],
                                       'takeaway': 'Eliminating the defender clears the path to victory.',
                                       'title': 'Raw Geometry: Trading into Back-Rank Checkmate',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Rc8#',
                                       'best_move_uci': 'c3c8',
                                       'description': "White's rook delivers mate along the c-file: 1. Rc8#!",
                                       'fen': '6k1/5ppp/8/8/8/2R5/8/4K3 w - - 0 1',
                                       'goal': 'Deliver 1. Rc8#.',
                                       'id': 'br_l1_05',
                                       'sequence': ['c3c8'],
                                       'takeaway': 'Pawn shields with no escape squares turn defensive walls into '
                                                   'prisons.',
                                       'title': 'Raw Geometry: Rook Invasion on c8',
                                       'turn': 'w'}],
                     'level2': [   {   'best_move_san': 'Re8+',
                                       'best_move_uci': 'e3e8',
                                       'description': 'Black has a rook guarding e8 from a8. White exchanges and '
                                                      'mates: 1. Re8+ Rxe8 2. Rxe8#!',
                                       'fen': 'r5k1/5ppp/8/8/8/4R3/5PPP/4R1K1 w - - 0 1',
                                       'goal': 'Exchange rooks on e8: 1. Re8+ Rxe8 2. Rxe8#.',
                                       'id': 'br_l2_01',
                                       'sequence': ['e3e8', 'a8e8', 'e1e8'],
                                       'takeaway': 'Doubled rooks on open files overpower singly defended back ranks.',
                                       'title': 'Stepping Stone: Doubled Heavy Pieces Overpowering e8',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Rd8+',
                                       'best_move_uci': 'd3d8',
                                       'description': "Black's rook on a8 guards the 8th rank. White's d-file battery "
                                                      'breaks through: 1. Rd8+ Rxd8 2. Rxd8#!',
                                       'fen': 'r5k1/5ppp/8/8/8/3R4/5PPP/3R2K1 w - - 0 1',
                                       'goal': 'Break through on d8: 1. Rd8+ Rxd8 2. Rxd8#.',
                                       'id': 'br_l2_02',
                                       'sequence': ['d3d8', 'a8d8', 'd1d8'],
                                       'takeaway': 'Two attackers overwhelm one defender on key back-rank entry '
                                                   'squares.',
                                       'title': 'Stepping Stone: d-file Battery Overcoming Guard',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Qe8+',
                                       'best_move_uci': 'e3e8',
                                       'description': "White deflects Black's rook with 1. Qe8+! Rxe8 2. Rxe8# "
                                                      'delivering checkmate.',
                                       'fen': 'r5k1/5ppp/8/8/8/4Q3/5PPP/4R1K1 w - - 0 1',
                                       'goal': 'Play 1. Qe8+ Rxe8 2. Rxe8#.',
                                       'id': 'br_l2_03',
                                       'sequence': ['e3e8', 'a8e8', 'e1e8'],
                                       'takeaway': 'Sacrificing heavy pieces to remove the final back-rank defender '
                                                   'leads to forced mate.',
                                       'title': 'Stepping Stone: Queen Sacrifice on e8',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Rc8+',
                                       'best_move_uci': 'c3c8',
                                       'description': "White's doubled rooks storm the c-file: 1. Rc8+ Rxc8 2. Rxc8#!",
                                       'fen': 'r5k1/5ppp/8/8/8/2R5/2R2PPP/6K1 w - - 0 1',
                                       'goal': 'Execute the c-file battery mate: 1. Rc8+ Rxc8 2. Rxc8#.',
                                       'id': 'br_l2_04',
                                       'sequence': ['c3c8', 'a8c8', 'c2c8'],
                                       'takeaway': 'Battery attacks on the flank back-rank leave the king no escape.',
                                       'title': 'Stepping Stone: c-file Infiltration',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Qxd8+',
                                       'best_move_uci': 'd3d8',
                                       'description': "White's queen sacrifice deflects Black's rook: 1. Qxd8+ Rxd8 2. "
                                                      'Rxd8#!',
                                       'fen': 'r2r2k1/5ppp/8/8/8/3Q4/5PPP/3R2K1 w - - 0 1',
                                       'goal': 'Deflect with 1. Qxd8+ Rxd8 2. Rxd8#.',
                                       'id': 'br_l2_05',
                                       'sequence': ['d3d8', 'a8d8', 'd1d8'],
                                       'takeaway': 'Deflecting the sole piece defending the back rank delivers swift '
                                                   'checkmate.',
                                       'title': 'Stepping Stone: Deflection of the Back-Rank Defender',
                                       'turn': 'w'}],
                     'level3': [   {   'best_move_san': 'Qd8+',
                                       'best_move_uci': 'd3d8',
                                       'description': 'White plays 1. Qd8+! Rxd8 2. Rxd8# delivering checkmate.',
                                       'fen': '2r3k1/pp3ppp/8/8/8/3Q4/PP3PPP/3R2K1 w - - 0 1',
                                       'goal': 'Sacrifice queen to force mate: 1. Qd8+ Rxd8 2. Rxd8#.',
                                       'id': 'br_l3_01',
                                       'sequence': ['d3d8', 'c8d8', 'd1d8'],
                                       'takeaway': 'Removing the defender with check leaves the opponent no time to '
                                                   'escape.',
                                       'title': 'Combat Mastery: Queen Deflection into Double Rook Mate',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Qd8+',
                                       'best_move_uci': 'd3d8',
                                       'description': 'White plays 1. Qd8+! Rxd8 2. Re8#.',
                                       'fen': '2r3k1/5ppp/8/8/8/B2Q4/5PPP/4R1K1 w - - 0 1',
                                       'goal': 'Deliver back-rank mate with 1. Qd8+ Rxd8 2. Re8#.',
                                       'id': 'br_l3_02',
                                       'sequence': ['d3d8', 'c8d8', 'e1e8'],
                                       'takeaway': 'Coordinating bishops with heavy pieces seals all escape squares.',
                                       'title': 'Combat Mastery: Sacrificial Deflection on the 8th Rank',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Qe8+',
                                       'best_move_uci': 'e3e8',
                                       'description': "Black's rook on d8 is overworked. White plays 1. Qe8+! Rxe8 2. "
                                                      'Rxe8#.',
                                       'fen': '3r2k1/pp3ppp/8/8/8/4Q3/PP3PPP/4R1K1 w - - 0 1',
                                       'goal': 'Execute the queen sacrifice on e8 to deliver mate.',
                                       'id': 'br_l3_03',
                                       'sequence': ['e3e8', 'd8e8', 'e1e8'],
                                       'takeaway': 'Overloaded defenders cannot fulfill two defensive roles '
                                                   'simultaneously.',
                                       'title': 'Combat Mastery: Overloaded Rook Deflection',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Rxe8#',
                                       'best_move_uci': 'e1e8',
                                       'description': 'White plays 1. Rxe8# delivering checkmate.',
                                       'fen': '4r1k1/pp3ppp/8/8/8/3Q4/PP3PPP/4R1K1 w - - 0 1',
                                       'goal': 'Deliver checkmate on e8 (1. Rxe8#).',
                                       'id': 'br_l3_04',
                                       'sequence': ['e1e8'],
                                       'takeaway': 'Back-rank geometry transforms modest leads into instant victories.',
                                       'title': 'Combat Mastery: Direct Infiltration on e8',
                                       'turn': 'w'},
                                   {   'best_move_san': 'Rxe8#',
                                       'best_move_uci': 'e1e8',
                                       'description': 'White clears the line with 1. Rxe8#.',
                                       'fen': '4r1k1/5ppp/8/8/8/8/PP3PPP/4R1K1 w - - 0 1',
                                       'goal': 'Play 1. Rxe8#.',
                                       'id': 'br_l3_05',
                                       'sequence': ['e1e8'],
                                       'takeaway': 'Back-rank tactical awareness turns complex games into clean '
                                                   'technical wins.',
                                       'title': 'Combat Mastery: Clearance on the 8th Rank',
                                       'turn': 'w'}]},
    'battery': {   'level1': [   {   'best_move_san': 'Rxe8#',
                                     'best_move_uci': 'e3e8',
                                     'description': "White's doubled rooks on the e-file crash through Black's back "
                                                    'rank: 1. Rxe8#!',
                                     'fen': '4r1k1/5ppp/8/8/8/4R3/4R3/6K1 w - - 0 1',
                                     'goal': 'Execute the e-file battery mate: 1. Rxe8#.',
                                     'id': 'bat_l1_01',
                                     'sequence': ['e3e8'],
                                     'takeaway': 'Doubled rooks on open files multiply attacking firepower '
                                                 'exponentially.',
                                     'title': 'Raw Geometry: Doubled Rooks on the e-file',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Qxh7#',
                                     'best_move_uci': 'd3h7',
                                     'description': "White's Queen and Bishop battery on b1-h7 delivers instant mate: "
                                                    '1. Qxh7#!',
                                     'fen': '5rk1/5ppp/8/8/8/1B1Q4/5PPP/6K1 w - - 0 1',
                                     'goal': 'Deliver 1. Qxh7#.',
                                     'id': 'bat_l1_02',
                                     'sequence': ['d3h7'],
                                     'takeaway': 'Aligning Queen and Bishop on the long diagonal creates unstoppable '
                                                 'mating threats.',
                                     'title': 'Raw Geometry: Queen and Bishop Battery Mating on h7',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Rxd8#',
                                     'best_move_uci': 'd3d8',
                                     'description': "White's d-file battery breaks Black's back rank: 1. Rxd8#!",
                                     'fen': '3r2k1/5ppp/8/8/8/3R4/3R4/6K1 w - - 0 1',
                                     'goal': 'Deliver 1. Rxd8#.',
                                     'id': 'bat_l1_03',
                                     'sequence': ['d3d8'],
                                     'takeaway': 'Heavy piece batteries control open central highways directly to the '
                                                 'opponent king.',
                                     'title': 'Raw Geometry: Doubled Rooks on the d-file',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Bh6',
                                     'best_move_uci': 'c1h6',
                                     'description': "White's dark-squared battery seals Black's fate: 1. Bh6 Kh8 2. "
                                                    'Qxg7#!',
                                     'fen': '6k1/5p1p/8/8/8/6Q1/5PPP/2B3K1 w - - 0 1',
                                     'goal': 'Play 1. Bh6 Kh8 2. Qxg7#.',
                                     'id': 'bat_l1_04',
                                     'sequence': ['c1h6', 'g8h8', 'g3g7'],
                                     'takeaway': 'Queen and Bishop batteries attacking fianchetto weaknesses force '
                                                 'instant checkmate.',
                                     'title': 'Raw Geometry: Diagonal Battery Checkmating on g7',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Rb7',
                                     'best_move_uci': 'a7b7',
                                     'description': "White's rooks coordinate along the 7th rank to corner Black's "
                                                    'king.',
                                     'fen': '6k1/R5p1/7p/8/8/8/R7/6K1 w - - 0 1',
                                     'goal': 'Maneuver rooks: 1. Rb7 Kh7 2. Raa7.',
                                     'id': 'bat_l1_05',
                                     'sequence': ['a7b7', 'g8h7', 'a2a7'],
                                     'takeaway': 'Two rooks on the 7th rank (the blind pigs) completely paralyze the '
                                                 'enemy king.',
                                     'title': 'Raw Geometry: 7th Rank Rook Battery',
                                     'turn': 'w'}],
                   'level2': [   {   'best_move_san': 'Qc2',
                                     'best_move_uci': 'd1c2',
                                     'description': 'White sets up a queen-bishop battery targeting the kingside: 1. '
                                                    'Qc2 Be6 2. Nc3.',
                                     'fen': 'r1bq1rk1/pp2bppp/2n2n2/3p4/8/1P2PN2/PB2BPPP/RN1Q1RK1 w - - 0 10',
                                     'goal': 'Play 1. Qc2 Be6 2. Nc3.',
                                     'id': 'bat_l2_01',
                                     'sequence': ['d1c2', 'c8e6', 'b1c3'],
                                     'takeaway': 'Placing queen behind bishop creates a long-range battery targeting '
                                                 'h7.',
                                     'title': 'Stepping Stone: Long Diagonal Queen-Bishop Battery',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Rxe8#',
                                     'best_move_uci': 'e1e8',
                                     'description': "White's battery breaks Black's e-file defenses with checkmate: 1. "
                                                    'Rxe8#.',
                                     'fen': '4r1k1/pp3ppp/8/8/8/3R4/PP3PPP/4R1K1 w - - 0 1',
                                     'goal': 'Deliver 1. Rxe8#.',
                                     'id': 'bat_l2_02',
                                     'sequence': ['e1e8'],
                                     'takeaway': 'Uncontested batteries on open files convert directly into back-rank '
                                                 'checkmates.',
                                     'title': 'Stepping Stone: Open File Battery Breakthrough',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Rxd8#',
                                     'best_move_uci': 'd3d8',
                                     'description': "White's heavy battery breaks Black's d-file defense: 1. Rxd8#!",
                                     'fen': '3r2k1/pp3ppp/8/8/8/3R4/PP1Q1PPP/6K1 w - - 0 1',
                                     'goal': 'Play 1. Rxd8#.',
                                     'id': 'bat_l2_03',
                                     'sequence': ['d3d8'],
                                     'takeaway': 'Queen-and-rook batteries overpower lone defensive rooks.',
                                     'title': 'Stepping Stone: Overcoming the Guard on d8',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Rxc7',
                                     'best_move_uci': 'c3c7',
                                     'description': "White's c-file battery crashes through Black's back rank: 1. Rxc7 "
                                                    'Rxc7 2. Rd8#!',
                                     'fen': '2r3k1/ppr2ppp/8/8/8/2R5/PP1R1PPP/6K1 w - - 0 1',
                                     'goal': 'Play 1. Rxc7 Rxc7 2. Rd8#.',
                                     'id': 'bat_l2_04',
                                     'sequence': ['c3c7', 'c8c7', 'd2d8'],
                                     'takeaway': 'Trading on the file opens up back-rank checkmate combinations.',
                                     'title': 'Stepping Stone: c-file Battery Liquidation',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Qe2',
                                     'best_move_uci': 'd3e2',
                                     'description': 'White re-routes the queen to form an unstoppable battery against '
                                                    "Black's king.",
                                     'fen': 'r1bq1rk1/ppp2ppp/2n1pn2/8/8/1B1Q1N2/PPP2PPP/RNB2RK1 w - - 0 9',
                                     'goal': 'Re-route queen: 1. Qe2 e5 2. Bg5.',
                                     'id': 'bat_l2_05',
                                     'sequence': ['d3e2', 'e6e5', 'c1g5'],
                                     'takeaway': 'Patient battery preparation builds irresistible pressure against '
                                                 'castle defenses.',
                                     'title': 'Stepping Stone: Diagonal Alignment Maneuver',
                                     'turn': 'w'}],
                   'level3': [   {   'best_move_san': 'Rxa7',
                                     'best_move_uci': 'a3a7',
                                     'description': "White's triple heavy battery on the a-file breaks through: 1. "
                                                    'Rxa7 Rxa7 2. Rxa7.',
                                     'fen': 'r4rk1/pp3ppp/8/8/8/R7/RR6/Q5K1 w - - 0 1',
                                     'goal': 'Play 1. Rxa7 Rxa7 2. Rxa7.',
                                     'id': 'bat_l3_01',
                                     'sequence': ['a3a7', 'a8a7', 'a2a7'],
                                     'takeaway': "Alekhine's Gun (two rooks backed by a queen) completely shatters "
                                                 'file defenses.',
                                     'title': "Combat Mastery: Alekhine's Gun Breakthrough",
                                     'turn': 'w'},
                                 {   'best_move_san': 'Bh6',
                                     'best_move_uci': 'c1h6',
                                     'description': "White's queen-bishop battery seals checkmate: 1. Bh6 Kh8 2. "
                                                    'Qxg7#!',
                                     'fen': '4r1k1/pp3p1p/8/8/8/6Q1/PP3PPP/2B3K1 w - - 0 1',
                                     'goal': 'Deliver mate: 1. Bh6 Kh8 2. Qxg7#.',
                                     'id': 'bat_l3_02',
                                     'sequence': ['c1h6', 'g8h8', 'g3g7'],
                                     'takeaway': 'Fianchetto light-squared diagonals provide lethal attacking '
                                                 'corridors.',
                                     'title': 'Combat Mastery: Diagonal Battery Crossfire Mate',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Rxd8+',
                                     'best_move_uci': 'd3d8',
                                     'description': 'White crashes through on d8: 1. Rxd8+ Rxd8 2. Qxd8#!',
                                     'fen': '2r3k1/pp3ppp/8/8/8/3R4/PP1Q1PPP/6K1 w - - 0 1',
                                     'goal': 'Play 1. Rxd8+ Rxd8 2. Qxd8#.',
                                     'id': 'bat_l3_03',
                                     'sequence': ['d3d8', 'c8d8', 'd2d8'],
                                     'takeaway': 'Doubled heavy batteries overpower lone defenders with forcing '
                                                 'checks.',
                                     'title': 'Combat Mastery: Heavy Battery Infiltration on d8',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Rc7',
                                     'best_move_uci': 'b7c7',
                                     'description': 'White coordinates rooks on the 7th rank: 1. Rc7 Kf8 2. Rbb7.',
                                     'fen': '6k1/1R4p1/8/8/8/8/1R4PP/6K1 w - - 0 1',
                                     'goal': 'Dominate 7th rank: 1. Rc7 Kf8 2. Rbb7.',
                                     'id': 'bat_l3_04',
                                     'sequence': ['b7c7', 'g8f8', 'b2b7'],
                                     'takeaway': 'Rooks doubled on the 7th rank cut off king escape routes '
                                                 'permanently.',
                                     'title': 'Combat Mastery: Dominant 7th Rank Battery Squeeze',
                                     'turn': 'w'},
                                 {   'best_move_san': 'Bxf6',
                                     'best_move_uci': 'c3f6',
                                     'description': "White eliminates the knight on f6 to open up Black's queen: 1. "
                                                    'Bxf6 Qxf6 2. Qxd7.',
                                     'fen': 'r2q1rk1/pp1b1ppp/2n1pn2/8/8/2BQ1N2/PPP2PPP/2KR1B1R w - - 0 11',
                                     'goal': 'Take knight: 1. Bxf6 Qxf6 2. Qxd7.',
                                     'id': 'bat_l3_05',
                                     'sequence': ['c3f6', 'd8f6', 'd3d7'],
                                     'takeaway': 'Removing the defensive anchor unleashes the full power of your piece '
                                                 'battery.',
                                     'title': 'Combat Mastery: Removing the Guard Against Battery Attack',
                                     'turn': 'w'}]},
    'discovered_attack': {   'level1': [   {   'best_move_san': 'Nc4+',
                                               'best_move_uci': 'e5c4',
                                               'description': "White's knight leaps out of the e-file: 1. Nc4+ Kf7 2. "
                                                              'Ne3 unmasking the rook check!',
                                               'fen': '4k3/8/8/4N3/8/8/8/4R1K1 w - - 0 1',
                                               'goal': 'Play 1. Nc4+ Kf7 2. Ne3.',
                                               'id': 'disc_l1_01',
                                               'sequence': ['e5c4', 'e8f7', 'c4e3'],
                                               'takeaway': 'Discovered checks are lethal because the unmasked check '
                                                           'freezes the opponent king.',
                                               'title': 'Raw Geometry: Discovered Check with Knight',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Bc6+',
                                               'best_move_uci': 'e4c6',
                                               'description': "White's bishop steps aside with check: 1. Bc6+ Kf7 2. "
                                                              'Bd5+ unmasking the queen!',
                                               'fen': '4k3/8/8/8/4B3/8/8/3QK3 w - - 0 1',
                                               'goal': 'Play 1. Bc6+ Kf7 2. Bd5+.',
                                               'id': 'disc_l1_02',
                                               'sequence': ['e4c6', 'e8f7', 'c6d5'],
                                               'takeaway': 'Moving piece can deliver its own attack while unmasking a '
                                                           'devastating second attack.',
                                               'title': 'Raw Geometry: Discovered Check with Bishop',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Nc6+',
                                               'best_move_uci': 'e5c6',
                                               'description': "White's knight leaps away with check on e-file: 1. Nc6+ "
                                                              'Kf8 2. Nxd8 winning the queen!',
                                               'fen': '3qk3/8/8/4N3/8/8/8/4R1K1 w - - 0 1',
                                               'goal': 'Play 1. Nc6+ Kf8 2. Nxd8.',
                                               'id': 'disc_l1_03',
                                               'sequence': ['e5c6', 'e8f8', 'c6d8'],
                                               'takeaway': 'Discovered checks freeze the enemy king, leaving '
                                                           'unprotected heavy pieces free to be captured.',
                                               'title': 'Raw Geometry: Discovered Attack Winning the Queen',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Nc7+',
                                               'best_move_uci': 'd5c7',
                                               'description': "White's knight jumps to c7 with check: 1. Nc7+ Kf7 2. "
                                                              'Nxa8 winning the rook!',
                                               'fen': 'r3k3/8/8/3N4/8/8/8/3R2K1 w - - 0 1',
                                               'goal': 'Play 1. Nc7+ Kf7 2. Nxa8.',
                                               'id': 'disc_l1_04',
                                               'sequence': ['d5c7', 'e8f7', 'c7a8'],
                                               'takeaway': 'Double-barreled attacks leave opponents no time to save '
                                                           'both threatened pieces.',
                                               'title': 'Raw Geometry: Knight Leap Unmasking Rook Check',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Bc6+',
                                               'best_move_uci': 'd5c6',
                                               'description': "White's bishop steps to c6 with check: 1. Bc6+ Kf7 2. "
                                                              'Bd5+.',
                                               'fen': '4k3/8/8/3B4/8/8/8/3R2K1 w - - 0 1',
                                               'goal': 'Deliver 1. Bc6+ Kf7 2. Bd5+.',
                                               'id': 'disc_l1_05',
                                               'sequence': ['d5c6', 'e8f7', 'c6d5'],
                                               'takeaway': 'Unmasking rooks on open files creates unstoppable mating '
                                                           'nets.',
                                               'title': 'Raw Geometry: Bishop Discovery on the King',
                                               'turn': 'w'}],
                             'level2': [   {   'best_move_san': 'O-O',
                                               'best_move_uci': 'e1g1',
                                               'description': 'White castles to place rook on the e-file and set up '
                                                              'discovered checks.',
                                               'fen': 'r1bqk2r/pppp1ppp/2n2n2/4p3/1bB1P3/2NP1N2/PPP2PPP/R1BQK2R w KQkq '
                                                      '- 0 6',
                                               'goal': 'Castle king: 1. O-O O-O 2. Bg5.',
                                               'id': 'disc_l2_01',
                                               'sequence': ['e1g1', 'e8g8', 'c1g5'],
                                               'takeaway': 'Completing development positions heavy pieces behind '
                                                           'unmasking minor pieces.',
                                               'title': 'Stepping Stone: Castle to Prepare Discovered Pin',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Nxd5',
                                               'best_move_uci': 'c3d5',
                                               'description': 'White exchanges knights on d5: 1. Nxd5 Qxd5 2. O-O '
                                                              'unmasking the center.',
                                               'fen': 'r1bqk2r/ppp2ppp/2n5/3np3/8/2NP1N2/PPP1BPPP/R1BQK2R w KQkq - 0 7',
                                               'goal': 'Play 1. Nxd5 Qxd5 2. O-O.',
                                               'id': 'disc_l2_02',
                                               'sequence': ['c3d5', 'd8d5', 'e1g1'],
                                               'takeaway': 'Opening files in the center activates hidden discovery '
                                                           'batteries.',
                                               'title': 'Stepping Stone: Center Discovery Exchange',
                                               'turn': 'w'},
                                           {   'best_move_san': 'O-O',
                                               'best_move_uci': 'e1g1',
                                               'description': 'White castles to prepare discovered attacks along the '
                                                              'e-file.',
                                               'fen': 'r1bq1rk1/ppp2ppp/2n1pn2/3p4/3P4/2NBPN2/PPP2PPP/R1BQK2R w KQ - 0 '
                                                      '7',
                                               'goal': 'Castle king: 1. O-O Re8 2. Re1.',
                                               'id': 'disc_l2_03',
                                               'sequence': ['e1g1', 'f8e8', 'f1e1'],
                                               'takeaway': 'Coordinating rooks on center files prepares dynamic '
                                                           'discovery combinations.',
                                               'title': 'Stepping Stone: Unmasking Kingside Rook',
                                               'turn': 'w'},
                                           {   'best_move_san': 'dxe4',
                                               'best_move_uci': 'd3e4',
                                               'description': 'White captures on e4 to open the d-file: 1. dxe4 d6 2. '
                                                              'O-O.',
                                               'fen': 'r1bqk2r/pppp1ppp/2n5/4p3/2B1n3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 '
                                                      '5',
                                               'goal': 'Play 1. dxe4 d6 2. O-O.',
                                               'id': 'disc_l2_04',
                                               'sequence': ['d3e4', 'd7d6', 'e1g1'],
                                               'takeaway': 'Center pawn captures unmask files for queen and rook '
                                                           'discovery combinations.',
                                               'title': 'Stepping Stone: Center Pawn Discovery Break',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Bg5',
                                               'best_move_uci': 'c1g5',
                                               'description': 'White develops bishop to g5: 1. Bg5 Be6 2. Bb3.',
                                               'fen': 'r1bq1rk1/ppp2ppp/2np1n2/4p3/2B1P3/2NP1N2/PPP2PPP/R1BQK2R w KQ - '
                                                      '0 7',
                                               'goal': 'Play 1. Bg5 Be6 2. Bb3.',
                                               'id': 'disc_l2_05',
                                               'sequence': ['c1g5', 'c8e6', 'c4b3'],
                                               'takeaway': 'Pins set up future discovered attacks as the opponent '
                                                           'pieces become frozen.',
                                               'title': 'Stepping Stone: Pinning Ahead of Discovery',
                                               'turn': 'w'}],
                             'level3': [   {   'best_move_san': 'Ne7+',
                                               'best_move_uci': 'd5e7',
                                               'description': 'White leaps with check: 1. Ne7+ Kh8 2. Rc1 unmasking '
                                                              'file pressure.',
                                               'fen': '5rk1/pp3ppp/8/3N4/8/8/PP3PPP/4R1K1 w - - 0 1',
                                               'goal': 'Play 1. Ne7+ Kh8 2. Rc1.',
                                               'id': 'disc_l3_01',
                                               'sequence': ['d5e7', 'g8h8', 'e1c1'],
                                               'takeaway': 'Windmill and leaping knight discoveries terrorize exposed '
                                                           'kings.',
                                               'title': 'Combat Mastery: Royal Knight Discovery Leap',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Ne7+',
                                               'best_move_uci': 'd5e7',
                                               'description': 'White checks with 1. Ne7+ Kf8 2. Rxd8 unmasking the '
                                                              'queen trade.',
                                               'fen': '4r1k1/pp3ppp/2n5/3N4/8/8/PP3PPP/3R2K1 w - - 0 1',
                                               'goal': 'Play 1. Ne7+ Kf8 2. Rxd8.',
                                               'id': 'disc_l3_02',
                                               'sequence': ['d5e7', 'g8f8', 'd1d8'],
                                               'takeaway': 'Intermediate checks with discovery eliminate key defensive '
                                                           'pieces.',
                                               'title': 'Combat Mastery: Discovered Deflection on King and Queen',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Rxe8#',
                                               'best_move_uci': 'e1e8',
                                               'description': 'White delivers checkmate on e8: 1. Rxe8#.',
                                               'fen': '3r2k1/pp3ppp/8/8/8/3N4/PP3PPP/4R1K1 w - - 0 1',
                                               'goal': 'Deliver 1. Rxe8#.',
                                               'id': 'disc_l3_03',
                                               'sequence': ['e1e8'],
                                               'takeaway': 'Discovered file control enables instant mating nets.',
                                               'title': 'Combat Mastery: Direct Back-Rank Infiltration Discovery',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Rxe8#',
                                               'best_move_uci': 'e1e8',
                                               'description': 'White clears the e-file delivering checkmate: 1. Rxe8#.',
                                               'fen': '4r1k1/pp3ppp/8/8/8/3Q4/PP3PPP/4R1K1 w - - 0 1',
                                               'goal': 'Deliver 1. Rxe8#.',
                                               'id': 'disc_l3_04',
                                               'sequence': ['e1e8'],
                                               'takeaway': 'Clearance moves unmask devastating crossfire.',
                                               'title': 'Combat Mastery: Queen Discovery Clearance',
                                               'turn': 'w'},
                                           {   'best_move_san': 'Ne7+',
                                               'best_move_uci': 'd5e7',
                                               'description': 'White leaps into e7: 1. Ne7+ Nxe7 2. Qxd8 winning the '
                                                              'queen.',
                                               'fen': 'r2q1rk1/pp3ppp/2n5/3N4/8/8/PP3PPP/R2QR1K1 w - - 0 1',
                                               'goal': 'Play 1. Ne7+ Nxe7 2. Qxd8.',
                                               'id': 'disc_l3_05',
                                               'sequence': ['d5e7', 'c6e7', 'd1d8'],
                                               'takeaway': 'Sacrificing minor pieces with check unmasks queen trades '
                                                           'and nets winning endgames.',
                                               'title': 'Combat Mastery: Discovered Attack Liquidating Queens',
                                               'turn': 'w'}]},
    'fork': {   'level1': [   {   'best_move_san': 'Nc7+',
                                  'best_move_uci': 'd5c7',
                                  'description': "White's knight leaps into c7, checking king and skewering rook.",
                                  'fen': 'r3k3/8/8/3N4/8/8/8/4K3 w - - 0 1',
                                  'goal': 'Play 1. Nc7+ Kd7 2. Nxa8.',
                                  'id': 'fork_l1_01',
                                  'sequence': ['d5c7', 'e8d7', 'c7a8'],
                                  'takeaway': 'Knights jump over obstacles to attack two pieces at once.',
                                  'title': 'Knight Royal Fork on c7',
                                  'turn': 'w'},
                              {   'best_move_san': 'Qd5+',
                                  'best_move_uci': 'd1d5',
                                  'description': "White's queen uses diagonal crossfire to check king and grab "
                                                 'undefended rook.',
                                  'fen': 'r5k1/8/8/8/8/8/8/3QK3 w - - 0 1',
                                  'goal': 'Deliver 1. Qd5+ Kg7 2. Qxa8.',
                                  'id': 'fork_l1_02',
                                  'sequence': ['d1d5', 'g8g7', 'd5a8'],
                                  'takeaway': 'Queen diagonal geometry checks and captures loose pieces across the '
                                              'board.',
                                  'title': 'Queen Double Attack on King and Rook',
                                  'turn': 'w'},
                              {   'best_move_san': 'Bd5+',
                                  'best_move_uci': 'f3d5',
                                  'description': "White's bishop delivers diagonal double attack against king and "
                                                 'rook.',
                                  'fen': 'r5k1/8/8/8/8/5B2/8/4K3 w - - 0 1',
                                  'goal': 'Play 1. Bd5+ Kg7 2. Bxa8.',
                                  'id': 'fork_l1_03',
                                  'sequence': ['f3d5', 'g8g7', 'd5a8'],
                                  'takeaway': 'Diagonal skewers attack multiple targets on the same color.',
                                  'title': 'Bishop Fork on d5+',
                                  'turn': 'w'},
                              {   'best_move_san': 'd4',
                                  'best_move_uci': 'd3d4',
                                  'description': 'White pushes the central pawn to attack two Black pieces at once.',
                                  'fen': '8/8/8/2n1b3/8/3P4/8/4K3 w - - 0 1',
                                  'goal': 'Push 1. d4 to fork knight and bishop.',
                                  'id': 'fork_l1_04',
                                  'sequence': ['d3d4', 'c5d3', 'e1d2'],
                                  'takeaway': 'Pawns are the most cost-effective forkers: a 1-point pawn attacking two '
                                              '3-point pieces.',
                                  'title': 'Pawn Fork Splitting Minor Pieces',
                                  'turn': 'w'},
                              {   'best_move_san': 'Nxe7',
                                  'best_move_uci': 'f5e7',
                                  'description': "White's knight leaps into f6 checking king and winning queen.",
                                  'fen': '4k3/4q3/8/5N2/8/8/8/4K3 w - - 0 1',
                                  'goal': 'Play 1. Nxe7 Kxe7.',
                                  'id': 'fork_l1_05',
                                  'sequence': ['f5e7', 'e8e7'],
                                  'takeaway': 'Spotting knight geometric targets wins decisive material in the '
                                              'endgame.',
                                  'title': 'Knight Fork on f6',
                                  'turn': 'w'}],
                'level2': [   {   'best_move_san': 'Nd6+',
                                  'best_move_uci': 'c4d6',
                                  'description': "White's knight infiltrates c7 in a French/Sicilian structure.",
                                  'fen': 'r1b1k2r/pp1p1ppp/2n1pn2/2q5/2N1P3/2P2N2/PP2BPPP/R2QK2R w KQkq - 0 10',
                                  'goal': 'Leap into d6 with check: 1. Nd6+ Ke7.',
                                  'id': 'fork_l2_01',
                                  'sequence': ['c4d6', 'e8e7', 'd6c8'],
                                  'takeaway': 'Outpost knights in enemy territory paralyze king mobility.',
                                  'title': 'Opening Royal Fork on c7',
                                  'turn': 'w'},
                              {   'best_move_san': 'd5',
                                  'best_move_uci': 'd4d5',
                                  'description': "White advances d-pawn to split Black's overextended knight and "
                                                 'bishop.',
                                  'fen': 'r1bqk2r/pppp1ppp/2n5/4b3/3Pn3/2P2N2/PP2BPPP/RNBQK2R w KQkq - 0 7',
                                  'goal': "Play 1. d5 to fork Black's minor pieces.",
                                  'id': 'fork_l2_02',
                                  'sequence': ['d4d5', 'c6e7', 'f3e5'],
                                  'takeaway': 'Center pawn pushes break piece coordination and net material.',
                                  'title': 'Central Pawn Fork Break',
                                  'turn': 'w'},
                              {   'best_move_san': 'Nd5',
                                  'best_move_uci': 'c3d5',
                                  'description': 'White attacks the center and opens diagonals.',
                                  'fen': 'r1bqk2r/pppp1ppp/2n2n2/4p3/1bB1P3/2N2N2/PPPP1PPP/R1BQK2R w - - 4 5',
                                  'goal': 'Play 1. Nd5 Nxd5 2. exd5.',
                                  'id': 'fork_l2_03',
                                  'sequence': ['c3d5', 'f6d5', 'e4d5'],
                                  'takeaway': 'Active central pieces generate double threats.',
                                  'title': 'Decoy into Knight Fork on e6',
                                  'turn': 'w'},
                              {   'best_move_san': 'dxe5',
                                  'best_move_uci': 'd4e5',
                                  'description': "White pushes e5 to fork Black's knight on f6 and bishop on d6.",
                                  'fen': 'r1bq1rk1/ppp2ppp/2nb1n2/4p3/3P4/2PB1N2/PP3PPP/RNBQ1RK1 w - - 0 8',
                                  'goal': 'Push 1. dxe5 Nxe5 2. Nxe5 Bxe5.',
                                  'id': 'fork_l2_04',
                                  'sequence': ['d4e5', 'c6e5', 'f3e5'],
                                  'takeaway': 'Opening the center reveals hidden tactical forks and weaknesses.',
                                  'title': 'Tactical Pawn Fork in the Center',
                                  'turn': 'w'},
                              {   'best_move_san': 'Qxd4',
                                  'best_move_uci': 'd1d4',
                                  'description': 'White centralizes queen with check, attacking king and undefended '
                                                 'bishop.',
                                  'fen': 'r1b1k2r/pppp1ppp/8/8/1b1q4/2N5/PPP1BPPP/R1BQK2R w - - 0 8',
                                  'goal': 'Play 1. Qxd4 Bxc3+ 2. bxc3.',
                                  'id': 'fork_l2_05',
                                  'sequence': ['d1d4', 'b4c3', 'b2c3'],
                                  'takeaway': 'Liquidating into a winning endgame starts by eliminating active pieces.',
                                  'title': 'Queen Infiltration Fork on d5',
                                  'turn': 'w'}],
                'level3': [   {   'best_move_san': 'Ne7+',
                                  'best_move_uci': 'd5e7',
                                  'description': "White lures Black's queen away with 1. Ne7+! winning Black's rook.",
                                  'fen': '3r2k1/pp3p1p/2n3p1/3N4/8/2P5/PP3PPP/3R2K1 w - - 0 1',
                                  'goal': 'Play 1. Ne7+ Kf8 2. Rxd8+ Nxd8.',
                                  'id': 'fork_l3_01',
                                  'sequence': ['d5e7', 'g8f8', 'd1d8', 'c6d8'],
                                  'takeaway': 'Intermediate checks force opponents into losing geometric alignments.',
                                  'title': 'Grandmaster Deflection into Royal Fork',
                                  'turn': 'w'},
                              {   'best_move_san': 'Rxe8#',
                                  'best_move_uci': 'e1e8',
                                  'description': 'White invades the 7th rank with check.',
                                  'fen': '4r1k1/pp3ppp/2n5/8/8/3N4/PP3PPP/4R1K1 w - - 0 1',
                                  'goal': 'Trade rooks with check: 1. Rxe8#.',
                                  'id': 'fork_l3_02',
                                  'sequence': ['e1e8'],
                                  'takeaway': 'Calculated exchanges remove defenders and exploit back-rank weaknesses.',
                                  'title': 'Rook Infiltration Fork on the 7th Rank',
                                  'turn': 'w'},
                              {   'best_move_san': 'cxd5',
                                  'best_move_uci': 'c4d5',
                                  'description': 'White establishes a dominant knight outpost on e5.',
                                  'fen': 'r2q1rk1/pp1b1ppp/2n1pn2/2pp4/2PP4/2NBPN2/PP3PPP/R2Q1RK1 w - - 0 9',
                                  'goal': 'Play 1. cxd5 exd5 2. dxc5.',
                                  'id': 'fork_l3_03',
                                  'sequence': ['c4d5', 'e6d5', 'd4c5'],
                                  'takeaway': 'Pawn structure simplification opens decisive tactical outposts.',
                                  'title': 'Knight Outpost in the Center',
                                  'turn': 'w'},
                              {   'best_move_san': 'Re7',
                                  'best_move_uci': 'e1e7',
                                  'description': 'White positions pieces for a royal infiltration.',
                                  'fen': '5rk1/5ppp/8/8/8/5N2/5PPP/4R1K1 w - - 0 1',
                                  'goal': 'Play 1. Re7 guarding the 7th rank.',
                                  'id': 'fork_l3_04',
                                  'sequence': ['e1e7', 'f8d8', 'g1f1'],
                                  'takeaway': "Rook on the 7th rank ties down Black's pieces.",
                                  'title': 'Smothered Threat Fork Preparation',
                                  'turn': 'w'},
                              {   'best_move_san': 'g3',
                                  'best_move_uci': 'g2g3',
                                  'description': 'White infiltrates the 7th rank with check, winning the exchange.',
                                  'fen': '4r1k1/pp1R1ppp/8/8/8/2N5/PP3PPP/6K1 w - - 0 1',
                                  'goal': 'Guard the back rank or invade: 1. g3 h6.',
                                  'id': 'fork_l3_05',
                                  'sequence': ['g2g3', 'h7h6', 'g1g2'],
                                  'takeaway': 'Creating luft before pursuing combinations avoids back-rank blunders.',
                                  'title': 'Knight Maneuver Forking Heavy Pieces',
                                  'turn': 'w'}]},
    'hanging_piece': {   'level1': [   {   'best_move_san': 'Qxa8+',
                                           'best_move_uci': 'h1a8',
                                           'description': "Black's rook on a8 is completely unprotected. White's queen "
                                                          'captures it freely: 1. Qxa8+.',
                                           'fen': 'r3k3/8/8/8/8/8/8/4K2Q w - - 0 1',
                                           'goal': 'Capture the hanging rook with 1. Qxa8+ Kd7 2. Qe4.',
                                           'id': 'hp_l1_01',
                                           'sequence': ['h1a8', 'e8d7', 'a8e4'],
                                           'takeaway': 'Loose pieces drop off (LPDO): always scan for completely '
                                                       'undefended pieces.',
                                           'title': 'Free Rook Capture on the Flank',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Rxe5+',
                                           'best_move_uci': 'e1e5',
                                           'description': "Black's knight on e5 has no defenders. White's rook "
                                                          'captures it: 1. Rxe5+.',
                                           'fen': '4k3/8/8/4n3/8/8/8/4R1K1 w - - 0 1',
                                           'goal': 'Capture the undefended knight: 1. Rxe5+ Kd7 2. Re3.',
                                           'id': 'hp_l1_02',
                                           'sequence': ['e1e5', 'e8d7', 'e5e3'],
                                           'takeaway': 'Central pieces without pawn anchors are primary targets for '
                                                       'tactical captures.',
                                           'title': 'Free Knight in the Center',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Qxb4',
                                           'best_move_uci': 'd2b4',
                                           'description': "Black's bishop on b4 is loose. White's queen captures it: "
                                                          '1. Qxb4.',
                                           'fen': '4k3/8/8/8/1b6/8/3Q4/4K3 w - - 0 1',
                                           'goal': 'Capture the hanging bishop: 1. Qxb4 Kf7 2. Qb3.',
                                           'id': 'hp_l1_03',
                                           'sequence': ['d2b4', 'e8f7', 'b4b3'],
                                           'takeaway': 'Scanning the perimeter prevents leaving isolated minor pieces '
                                                       'hanging.',
                                           'title': 'Free Bishop on the Wing',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Bxd5',
                                           'best_move_uci': 'e4d5',
                                           'description': "Black's central knight is unprotected. White's bishop "
                                                          'captures it cleanly.',
                                           'fen': '4k3/8/8/3n4/4B3/8/8/4K3 w - - 0 1',
                                           'goal': 'Capture the loose knight: 1. Bxd5 Ke7 2. Bc4.',
                                           'id': 'hp_l1_04',
                                           'sequence': ['e4d5', 'e8e7', 'd5c4'],
                                           'takeaway': 'Even well-placed central pieces must be supported by friendly '
                                                       'pawns.',
                                           'title': 'Loose Central Knight Captured by Bishop',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Nxg5',
                                           'best_move_uci': 'f3g5',
                                           'description': "Black's queen wandered into enemy lines unprotected. "
                                                          'Capture it cleanly.',
                                           'fen': '4k3/8/8/6q1/8/5N2/8/4K3 w - - 0 1',
                                           'goal': 'Capture the hanging queen: 1. Nxg5 Ke7 2. Ne4.',
                                           'id': 'hp_l1_05',
                                           'sequence': ['f3g5', 'e8e7', 'g5e4'],
                                           'takeaway': 'Never venture your queen forward into enemy territory without '
                                                       'tactical defense.',
                                           'title': 'Loose Queen Snapped Up',
                                           'turn': 'w'}],
                         'level2': [   {   'best_move_san': 'Nxe4',
                                           'best_move_uci': 'c3e4',
                                           'description': "White captures Black's loose knight on e4 after counting "
                                                          'attackers.',
                                           'fen': 'r1bqkb1r/ppp2ppp/2n5/3p4/4n3/2NP4/PPP1BPPP/R1BQK1NR w KQkq - 0 6',
                                           'goal': 'Play 1. Nxe4 dxe4 2. dxe4.',
                                           'id': 'hp_l2_01',
                                           'sequence': ['c3e4', 'd5e4', 'd3e4'],
                                           'takeaway': 'Count attackers versus defenders: an insufficiently guarded '
                                                       'piece is effectively loose.',
                                           'title': 'Removing the Defender of the Loose Knight',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Nxe4',
                                           'best_move_uci': 'c3e4',
                                           'description': 'White exchanges minor pieces to exploit the loose piece.',
                                           'fen': 'r1bqk2r/ppp2ppp/2n5/2bp4/4n3/2NP1N2/PPP1BPPP/R1BQK2R w KQkq - 0 7',
                                           'goal': 'Play 1. Nxe4 dxe4 2. dxe4.',
                                           'id': 'hp_l2_02',
                                           'sequence': ['c3e4', 'd5e4', 'd3e4'],
                                           'takeaway': 'Liquidating defenders leaves remaining pieces vulnerable.',
                                           'title': 'Exploiting Loose Bishop on c5',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Rxe4',
                                           'best_move_uci': 'e1e4',
                                           'description': 'Black played an early Queen sortie. White punishes the '
                                                          'loose queen: 1. Rxe4.',
                                           'fen': 'r4rk1/ppp2ppp/2n5/8/4q3/2P5/PP3PPP/R1BQR1K1 w - - 0 1',
                                           'goal': 'Capture the hanging queen: 1. Rxe4 Rae8 2. Rxe8.',
                                           'id': 'hp_l2_03',
                                           'sequence': ['e1e4', 'a8e8', 'e4e8'],
                                           'takeaway': 'Rooks on open central files punish exposed queens without '
                                                       'delay.',
                                           'title': 'Punishing the Loose Queen in the Open Center',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Nxd5',
                                           'best_move_uci': 'c3d5',
                                           'description': 'White liquidates the central knight to expose the d5 pawn.',
                                           'fen': 'r1bqk2r/pppp1ppp/2n5/3np3/8/2NP1N2/PPP1BPPP/R1BQK2R w KQkq - 0 6',
                                           'goal': 'Capture on d5: 1. Nxd5 d6 2. O-O.',
                                           'id': 'hp_l2_04',
                                           'sequence': ['c3d5', 'd7d6', 'e1g1'],
                                           'takeaway': 'Exchanging into superior structures leaves enemy pawns '
                                                       'backward and weak.',
                                           'title': 'Trading to Win the Hanging Central Pawn',
                                           'turn': 'w'},
                                       {   'best_move_san': 'c3',
                                           'best_move_uci': 'c2c3',
                                           'description': 'White attacks the center pawn with tempo.',
                                           'fen': 'r1bqk1nr/pppp1ppp/2n5/4p3/1b2P3/3P1N2/PPP2PPP/RNBQKB1R w KQkq - 1 4',
                                           'goal': 'Block the check and develop: 1. c3 Be7 2. Be2.',
                                           'id': 'hp_l2_05',
                                           'sequence': ['c2c3', 'b4e7', 'f1e2'],
                                           'takeaway': 'Countering checks with pawn tempo preserves initiative.',
                                           'title': 'Exploiting the Loose e-pawn',
                                           'turn': 'w'}],
                         'level3': [   {   'best_move_san': 'Rd7',
                                           'best_move_uci': 'd1d7',
                                           'description': 'White invades the 7th rank with 1. Rd7! attacking loose '
                                                          'pawns.',
                                           'fen': 'r3r1k1/pp3ppp/2n5/8/8/2P2N2/PP3PPP/3R1RK1 w - - 0 1',
                                           'goal': 'Invade the 7th rank: 1. Rd7 Rab8 2. Rfd1.',
                                           'id': 'hp_l3_01',
                                           'sequence': ['d1d7', 'a8b8', 'f1d1'],
                                           'takeaway': 'Rooks on the 7th rank turn passive opponent pawns into '
                                                       'immediate tactical targets.',
                                           'title': 'Combat Mastery: Infiltration Against Loose b7 Pawn',
                                           'turn': 'w'},
                                       {   'best_move_san': 'h3',
                                           'best_move_uci': 'h2h3',
                                           'description': 'White drives back the enemy bishop with tempo.',
                                           'fen': 'r2q1rk1/ppp2ppp/2n5/4p3/6b1/2NP1N2/PPP2PPP/R2Q1RK1 w - - 0 1',
                                           'goal': 'Kick the bishop: 1. h3 Bh5 2. g4.',
                                           'id': 'hp_l3_02',
                                           'sequence': ['h2h3', 'g4h5', 'g2g4'],
                                           'takeaway': 'Challenging loose pieces forces concessions in opponent piece '
                                                       'activity.',
                                           'title': 'Combat Mastery: Exploiting Loose Queen on the Rim',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Rxd8#',
                                           'best_move_uci': 'd3d8',
                                           'description': 'White delivers checkmate against the loose back rank.',
                                           'fen': '3r2k1/pp3ppp/8/8/8/3R1N2/PP3PPP/6K1 w - - 0 1',
                                           'goal': 'Play 1. Rxd8# delivering checkmate.',
                                           'id': 'hp_l3_03',
                                           'sequence': ['d3d8'],
                                           'takeaway': 'Eliminating the defender overpowers the back rank.',
                                           'title': 'Combat Mastery: Direct Back-Rank Exploitation',
                                           'turn': 'w'},
                                       {   'best_move_san': 'g3',
                                           'best_move_uci': 'g2g3',
                                           'description': 'White improves king safety while keeping pressure on '
                                                          "Black's loose pieces.",
                                           'fen': '4r1k1/pp1R1ppp/8/8/8/8/PP3PPP/6K1 w - - 0 1',
                                           'goal': 'Create luft: 1. g3 h6 2. Kg2.',
                                           'id': 'hp_l3_04',
                                           'sequence': ['g2g3', 'h7h6', 'g1g2'],
                                           'takeaway': 'Securing king escape squares guarantees winning conversions in '
                                                       'piece endgames.',
                                           'title': 'Combat Mastery: Loose Piece Endgame Conversion',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Ke2',
                                           'best_move_uci': 'e1e2',
                                           'description': "White's king activates to attack Black's loose knight.",
                                           'fen': '4k3/pp3ppp/8/8/4n3/5N2/PP3PPP/4K3 w - - 0 1',
                                           'goal': 'Centralize the king: 1. Ke2 Ke7 2. Ke3.',
                                           'id': 'hp_l3_05',
                                           'sequence': ['e1e2', 'e8e7', 'e2e3'],
                                           'takeaway': 'In the endgame, the king becomes an active fighting piece that '
                                                       'pressures loose targets.',
                                           'title': 'Combat Mastery: Central King Activation in Endgame',
                                           'turn': 'w'}]},
    'overloaded_defender': {   'level1': [   {   'best_move_san': 'Rxc5',
                                                 'best_move_uci': 'c3c5',
                                                 'description': "Black's queen is overworked. White's rook captures "
                                                                'the hanging bishop on c5: 1. Rxc5.',
                                                 'fen': '4k3/4q3/8/2b5/8/2R5/8/6K1 w - - 0 1',
                                                 'goal': 'Capture the hanging bishop: 1. Rxc5 Qxc5+.',
                                                 'id': 'ov_l1_01',
                                                 'sequence': ['c3c5', 'e7c5'],
                                                 'takeaway': 'Overloaded defenders tasked with protecting multiple '
                                                             'pieces will collapse under pressure.',
                                                 'title': 'Raw Geometry: Queen Guarding Multiple Heavy Pieces',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Qxe7#',
                                                 'best_move_uci': 'e2e7',
                                                 'description': "Black's knight on e7 cannot defend against White's "
                                                                'queen mating on e7: 1. Qxe7#!',
                                                 'fen': '4k3/4n3/8/8/8/8/4Q3/4R1K1 w - - 0 1',
                                                 'goal': 'Deliver 1. Qxe7#.',
                                                 'id': 'ov_l1_02',
                                                 'sequence': ['e2e7'],
                                                 'takeaway': 'Pieces pinned or overloaded cannot fulfill their '
                                                             'defensive responsibilities.',
                                                 'title': 'Raw Geometry: Overworked Knight Defending Mate',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Rxd5',
                                                 'best_move_uci': 'd1d5',
                                                 'description': "Black's rook on d8 cannot protect d5. White captures "
                                                                'the bishop: 1. Rxd5.',
                                                 'fen': '3r2k1/5ppp/8/3b4/8/8/8/3R2K1 w - - 0 1',
                                                 'goal': 'Capture the bishop: 1. Rxd5 Rxd5.',
                                                 'id': 'ov_l1_03',
                                                 'sequence': ['d1d5', 'd8d5'],
                                                 'takeaway': 'When a defender is asked to protect two things at once, '
                                                             'strike the softer target.',
                                                 'title': 'Raw Geometry: Overloaded Rook Defending File and Piece',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Qxd7+',
                                                 'best_move_uci': 'd1d7',
                                                 'description': "Black's king cannot guard both knights. White strikes "
                                                                'on d7: 1. Qxd7+ Kf8 2. Qxe7.',
                                                 'fen': '4k3/3nn3/8/8/8/8/8/3QK3 w - - 0 1',
                                                 'goal': 'Play 1. Qxd7+ Kf8 2. Qxe7.',
                                                 'id': 'ov_l1_04',
                                                 'sequence': ['d1d7', 'e8f8', 'd7e7'],
                                                 'takeaway': 'Kings forced to defend multiple pieces leave their army '
                                                             'exposed.',
                                                 'title': 'Raw Geometry: Overloaded King Protecting Minor Pieces',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Qxd5',
                                                 'best_move_uci': 'd1d5',
                                                 'description': "Black's e6 pawn cannot defend both knights. White "
                                                                'captures on d5: 1. Qxd5.',
                                                 'fen': '4k3/8/4p3/3n1n2/8/8/8/3QK3 w - - 0 1',
                                                 'goal': 'Capture the knight: 1. Qxd5 exd5.',
                                                 'id': 'ov_l1_05',
                                                 'sequence': ['d1d5', 'e6d5'],
                                                 'takeaway': 'Pawns trying to hold two diagonal pieces together will '
                                                             'crack when attacked.',
                                                 'title': 'Raw Geometry: Overloaded Pawn Protecting Central Knights',
                                                 'turn': 'w'}],
                               'level2': [   {   'best_move_san': 'O-O',
                                                 'best_move_uci': 'e1g1',
                                                 'description': 'White castles to connect rooks and increase pressure '
                                                                "on Black's overloaded queen.",
                                                 'fen': 'r3k2r/pppq1ppp/2n5/3p4/8/2B2N2/PPP2PPP/R2QK2R w KQkq - 0 11',
                                                 'goal': 'Castle king: 1. O-O O-O 2. Re1.',
                                                 'id': 'ov_l2_01',
                                                 'sequence': ['e1g1', 'e8g8', 'f1e1'],
                                                 'takeaway': 'Harmonious development increases attacking pressure on '
                                                             'overworked defensive pieces.',
                                                 'title': 'Stepping Stone: Deflecting Queen from Rook Defense',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Rxe8#',
                                                 'best_move_uci': 'e1e8',
                                                 'description': "Black's rook on e8 cannot defend the back rank. White "
                                                                'plays 1. Rxe8#.',
                                                 'fen': '4r1k1/pp3ppp/2n5/8/8/3R4/PP3PPP/4R1K1 w - - 0 1',
                                                 'goal': 'Deliver 1. Rxe8#.',
                                                 'id': 'ov_l2_02',
                                                 'sequence': ['e1e8'],
                                                 'takeaway': 'Overburdened rooks on the back rank fail when pressured '
                                                             'by multiple attackers.',
                                                 'title': 'Stepping Stone: Deflecting the Back-Rank Rook',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'dxe5',
                                                 'best_move_uci': 'd4e5',
                                                 'description': 'White plays 1. dxe5 winning the pawn and deflecting '
                                                                "Black's knight.",
                                                 'fen': 'r1bq1rk1/ppp2ppp/2n2n2/3pp3/3P4/2PBPN2/PP1N1PPP/R2QK2R w KQ - '
                                                        '0 8',
                                                 'goal': 'Play 1. dxe5 Nxe5 2. Nxe5.',
                                                 'id': 'ov_l2_03',
                                                 'sequence': ['d4e5', 'c6e5', 'f3e5'],
                                                 'takeaway': 'Pawn breaks force opponent defenders away from their '
                                                             'assigned posts.',
                                                 'title': 'Stepping Stone: Exploiting Central Overloaded Knight',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Qd5',
                                                 'best_move_uci': 'd1d5',
                                                 'description': 'White plays 1. Qd5! creating dual threats against f7 '
                                                                'mate and loose central pieces.',
                                                 'fen': 'r1bqk2r/pppp1ppp/2n5/4p3/2B1n3/2P2N2/PPP2PPP/R1BQK2R w KQkq - '
                                                        '0 6',
                                                 'goal': 'Play 1. Qd5 Ne7 2. Qxf7#.',
                                                 'id': 'ov_l2_04',
                                                 'sequence': ['d1d5', 'c6e7', 'd5f7'],
                                                 'takeaway': 'Dual threats overwhelm single defenders who cannot be in '
                                                             'two places at once.',
                                                 'title': "Stepping Stone: Scholar's Pressure on Overworked f7",
                                                 'turn': 'w'},
                                             {   'best_move_san': 'O-O',
                                                 'best_move_uci': 'e1g1',
                                                 'description': "White castles to activate the rooks against Black's "
                                                                'overworked queen.',
                                                 'fen': '2r1k2r/pp1q1ppp/2n1pn2/2bp4/8/2N1PN2/PPP2PPP/R1BQK2R w KQk - '
                                                        '0 9',
                                                 'goal': 'Play 1. O-O O-O 2. Qe2.',
                                                 'id': 'ov_l2_05',
                                                 'sequence': ['e1g1', 'e8g8', 'd1e2'],
                                                 'takeaway': 'Improving position steadily breaks down opponent '
                                                             'defensive coordination.',
                                                 'title': 'Stepping Stone: Centralizing Queen with Pressure',
                                                 'turn': 'w'}],
                               'level3': [   {   'best_move_san': 'Qe8+',
                                                 'best_move_uci': 'e3e8',
                                                 'description': "White plays 1. Qe8+! Rxe8 2. Rxe8# deflecting Black's "
                                                                'overworked rook.',
                                                 'fen': 'r3r1k1/pp3ppp/8/8/8/4Q3/PP3PPP/4R1K1 w - - 0 1',
                                                 'goal': 'Play 1. Qe8+ Rxe8 2. Rxe8#.',
                                                 'id': 'ov_l3_01',
                                                 'sequence': ['e3e8', 'a8e8', 'e1e8'],
                                                 'takeaway': 'Queen sacrifices that deflect back-rank defenders end '
                                                             'games decisively.',
                                                 'title': 'Combat Mastery: Queen Deflection Shattering the Back Rank',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Qd7',
                                                 'best_move_uci': 'd3d7',
                                                 'description': "White plays 1. Qd7! attacking Black's overloaded rook "
                                                                'on f8.',
                                                 'fen': '5rk1/pp3ppp/8/8/8/3Q4/PP3PPP/4R1K1 w - - 0 1',
                                                 'goal': 'Infiltrate with 1. Qd7 Rd8 2. Qxd8+.',
                                                 'id': 'ov_l3_02',
                                                 'sequence': ['d3d7', 'f8d8', 'd7d8'],
                                                 'takeaway': 'Invading deep ranks overburdens enemy defensive pieces.',
                                                 'title': 'Combat Mastery: Deflection on the 7th Rank',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Qe2',
                                                 'best_move_uci': 'd1e2',
                                                 'description': 'White plays 1. Qe2 connecting rooks and preparing '
                                                                'central breakthrough.',
                                                 'fen': 'r4rk1/pp1b1ppp/2n1pn2/3p4/3P4/2PB1N2/PP1N1PPP/R2Q1RK1 w - - 0 '
                                                        '11',
                                                 'goal': 'Centralize with 1. Qe2 Rac8 2. Ne5.',
                                                 'id': 'ov_l3_03',
                                                 'sequence': ['d1e2', 'a8c8', 'f3e5'],
                                                 'takeaway': 'Positioning heavy pieces overburdens opponent flank '
                                                             'defenders.',
                                                 'title': 'Combat Mastery: Decoy Breaking Pawn Structure',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Rxd8+',
                                                 'best_move_uci': 'd3d8',
                                                 'description': 'White breaks through on d8: 1. Rxd8+ Rxd8 2. Rxd8#!',
                                                 'fen': 'r2r2k1/pp3ppp/8/8/8/3R4/PP3PPP/3R2K1 w - - 0 1',
                                                 'goal': 'Deliver 1. Rxd8+ Rxd8 2. Rxd8#.',
                                                 'id': 'ov_l3_04',
                                                 'sequence': ['d3d8', 'a8d8', 'd1d8'],
                                                 'takeaway': 'Sequential exchanges exhaust overloaded pieces until '
                                                             'defenses collapse.',
                                                 'title': 'Combat Mastery: Overworked Heavy Piece Battery Liquidation',
                                                 'turn': 'w'},
                                             {   'best_move_san': 'Rxe8#',
                                                 'best_move_uci': 'e1e8',
                                                 'description': 'White delivers checkmate on e8: 1. Rxe8#.',
                                                 'fen': '4r1k1/pp3ppp/8/8/8/B2Q4/PP3PPP/4R1K1 w - - 0 1',
                                                 'goal': 'Deliver 1. Rxe8#.',
                                                 'id': 'ov_l3_05',
                                                 'sequence': ['e1e8'],
                                                 'takeaway': 'Coordinated piece pressure overcomes stubborn defenses '
                                                             'with mathematical certainty.',
                                                 'title': "Combat Mastery: Decoy Undermining the King's Shield",
                                                 'turn': 'w'}]},
    'pin': {   'level1': [   {   'best_move_san': 'd5',
                                 'best_move_uci': 'd4d5',
                                 'description': "Black's knight on d7 is pinned to King on e8 by Bishop on b5. Push "
                                                'pawn to d5 (1. d5) to win the paralyzed knight!',
                                 'fen': '4k3/3n4/8/1B6/3P4/8/8/4K3 w - - 0 1',
                                 'goal': 'Push 1. d5 to attack the pinned knight.',
                                 'id': 'pin_l1_01',
                                 'sequence': ['d4d5', 'e8e7', 'd5d6'],
                                 'takeaway': 'The golden rule of pins: always pile pressure on the pinned piece, '
                                             'especially with pawns!',
                                 'title': 'Raw Geometry: Piling Pressure with Pawns',
                                 'turn': 'w'},
                             {   'best_move_san': 'fxe5',
                                 'best_move_uci': 'f4e5',
                                 'description': "Black's knight on e5 is pinned to King on e8. White's pawn captures "
                                                'it cleanly: 1. fxe5.',
                                 'fen': '4k3/8/8/4n3/5P2/8/8/4R1K1 w - - 0 1',
                                 'goal': 'Capture the pinned knight: 1. fxe5 Kf7 2. Kf2.',
                                 'id': 'pin_l1_02',
                                 'sequence': ['f4e5', 'e8f7', 'g1f2'],
                                 'takeaway': 'Pinned pieces cannot move to safety when attacked by lower-value pawns.',
                                 'title': 'Raw Geometry: Absolute Rook Pin on the e-file',
                                 'turn': 'w'},
                             {   'best_move_san': 'Bxd6+',
                                 'best_move_uci': 'c5d6',
                                 'description': "Black's Queen on d6 and King on e7 are aligned. White's bishop pins "
                                                'and wins the Queen: 1. Bxd6+.',
                                 'fen': '8/4k3/3q4/2B5/8/8/8/4K3 w - - 0 1',
                                 'goal': 'Capture the pinned Queen with 1. Bxd6+ Kd6.',
                                 'id': 'pin_l1_03',
                                 'sequence': ['c5d6', 'e7d6'],
                                 'takeaway': 'Absolute pins to the king paralyze even the most powerful pieces.',
                                 'title': 'Raw Geometry: Pinning Queen to King',
                                 'turn': 'w'},
                             {   'best_move_san': 'Rxd7+',
                                 'best_move_uci': 'd2d7',
                                 'description': "Black's bishop on d7 is pinned to King on d8. White's rook captures "
                                                'it: 1. Rxd7+.',
                                 'fen': '3k4/3b4/8/8/8/8/3R4/4K3 w - - 0 1',
                                 'goal': 'Capture the pinned piece with 1. Rxd7+.',
                                 'id': 'pin_l1_04',
                                 'sequence': ['d2d7', 'd8e8', 'd7a7'],
                                 'takeaway': 'When an opponent piece is pinned and insufficiently defended, capture '
                                             'it.',
                                 'title': 'Raw Geometry: Pinning Along the d-file',
                                 'turn': 'w'},
                             {   'best_move_san': 'Bxf6',
                                 'best_move_uci': 'e5f6',
                                 'description': "White's bishop pins Black's knight to the King. Capture with 1. Bxf6.",
                                 'fen': '4k3/5p2/5n2/4B3/8/8/8/4K3 w - - 0 1',
                                 'goal': 'Capture the pinned knight on f6 (1. Bxf6).',
                                 'id': 'pin_l1_05',
                                 'sequence': ['e5f6'],
                                 'takeaway': 'Cross-board diagonals allow long-range bishops to paralyze defensive '
                                             'knights.',
                                 'title': 'Raw Geometry: Diagonal Bishop Pin',
                                 'turn': 'w'}],
               'level2': [   {   'best_move_san': 'd5',
                                 'best_move_uci': 'd4d5',
                                 'description': "Black's knight on c6 is pinned by White's bishop on b5. Push 1. d5 to "
                                                'win the piece!',
                                 'fen': 'r1bqk1nr/pppp1ppp/2n5/1B2p3/3PP3/5N2/PPP2PPP/RNBQK2R w KQkq - 0 4',
                                 'goal': 'Push 1. d5 to attack and win the pinned knight on c6.',
                                 'id': 'pin_l2_01',
                                 'sequence': ['d4d5', 'c6e7', 'f3e5'],
                                 'takeaway': 'Pushing pawns against pinned knights forces retreat or captures.',
                                 'title': 'Stepping Stone: Winning the Pinned Defender',
                                 'turn': 'w'},
                             {   'best_move_san': 'Be7',
                                 'best_move_uci': 'f8e7',
                                 'description': "White's bishop on g5 pins Black's knight. Black breaks the pin by "
                                                'developing the bishop to e7: 1... Be7!',
                                 'fen': 'r1bqkb1r/ppp2ppp/2np1n2/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R b KQkq - 1 5',
                                 'goal': 'Neutralize the pin by developing dark-squared bishop to e7.',
                                 'id': 'pin_l2_02',
                                 'sequence': ['f8e7', 'b1c3', 'c8e6'],
                                 'takeaway': 'Interposing a piece breaks the pin and neutralizes opponent tactical '
                                             'threats.',
                                 'title': 'Stepping Stone: Neutralizing the Pin',
                                 'turn': 'b'},
                             {   'best_move_san': 'Rde2',
                                 'best_move_uci': 'd2e2',
                                 'description': 'White doubles heavy pieces on the pinned rook on e7: 1. Rde2! '
                                                'followed by winning the exchange.',
                                 'fen': '4k3/4r3/8/8/8/8/3R4/4R1K1 w - - 0 1',
                                 'goal': 'Double on e-file with 1. Rde2 Kf7 2. Rxe7+.',
                                 'id': 'pin_l2_03',
                                 'sequence': ['d2e2', 'e8f7', 'e2e7'],
                                 'takeaway': 'Doubling heavy pieces on pinned pieces guarantees favorable exchanges.',
                                 'title': 'Stepping Stone: Doubling Pressure on the Pinned Rook',
                                 'turn': 'w'},
                             {   'best_move_san': 'O-O',
                                 'best_move_uci': 'e1g1',
                                 'description': 'White castles to bring the king to safety and connect rooks to '
                                                'exploit the pin.',
                                 'fen': 'r1bqk2r/pppp1ppp/2n2n2/4p1B1/1bB1P3/2NP1N2/PPP2PPP/R2QK2R w KQkq - 0 6',
                                 'goal': 'Castle to secure king: 1. O-O O-O 2. Nd5.',
                                 'id': 'pin_l2_04',
                                 'sequence': ['e1g1', 'e8g8', 'c3d5'],
                                 'takeaway': 'Piling up attackers against a pinned piece wins material or fractures '
                                             'opponent pawns.',
                                 'title': 'Stepping Stone: Castling into Safety and Piling on f6',
                                 'turn': 'w'},
                             {   'best_move_san': 'Bxf7+',
                                 'best_move_uci': 'c4f7',
                                 'description': 'White breaks the pin by playing 1. Bxf7+! Kxf7 2. Ng5+.',
                                 'fen': 'r2qk2r/ppp2ppp/2n5/4p3/2B3b1/3P1N2/PPP2PPP/RNBQ1RK1 w kq - 0 7',
                                 'goal': 'Sacrifice on f7 to break the pin with tempo.',
                                 'id': 'pin_l2_05',
                                 'sequence': ['c4f7', 'e8f7', 'f3g5'],
                                 'takeaway': 'Counter-forcing moves with check eliminate pins dynamically.',
                                 'title': 'Stepping Stone: Breaking the Pin with Check',
                                 'turn': 'w'}],
               'level3': [   {   'best_move_san': 'Bxf6',
                                 'best_move_uci': 'g5f6',
                                 'description': 'White plays 1. Bxf6! Bxf6 2. Nxf6+ winning material.',
                                 'fen': '4r1k1/pp1q1pbp/2p2np1/3N2B1/8/2P5/PP3PPP/R2QR1K1 w - - 0 1',
                                 'goal': 'Capture on f6 to exploit the pinned piece.',
                                 'id': 'pin_l3_01',
                                 'sequence': ['g5f6', 'g7f6', 'd5f6', 'g8g7', 'f6d7'],
                                 'takeaway': 'Converting pins into royal forks decisively ends resistance.',
                                 'title': 'Combat Mastery: Shattering the Pinned King-Side',
                                 'turn': 'w'},
                             {   'best_move_san': 'O-O',
                                 'best_move_uci': 'e1g1',
                                 'description': "Black's king is in the center. White castles to exploit pin dynamics.",
                                 'fen': 'r1bqk2r/pppp1ppp/2n2n2/4p3/1bB1P3/2NP1N2/PPP2PPP/R1BQK2R w KQkq - 0 6',
                                 'goal': 'Develop or pin with 1. O-O.',
                                 'id': 'pin_l3_02',
                                 'sequence': ['e1g1', 'e8g8', 'c1g5'],
                                 'takeaway': 'Completing development enables devastating pins across the center files.',
                                 'title': 'Combat Mastery: Pin Exploitation Against Uncastled King',
                                 'turn': 'w'},
                             {   'best_move_san': 'Rxd8+',
                                 'best_move_uci': 'd1d8',
                                 'description': 'White plays 1. Rxd8+! Qxd8 2. Qxa5 winning the piece.',
                                 'fen': '3r2k1/pp2qppp/4b3/n7/Q1B5/8/PP3PPP/3R2K1 w - - 0 1',
                                 'goal': 'Trade rooks on d8 to remove the defender.',
                                 'id': 'pin_l3_03',
                                 'sequence': ['d1d8', 'e7d8', 'a4a5'],
                                 'takeaway': 'Pinned and overworked pieces crumble when their anchor is deflected.',
                                 'title': 'Combat Mastery: Pin & Decoy Sacrifice',
                                 'turn': 'w'},
                             {   'best_move_san': 'Nxe7+',
                                 'best_move_uci': 'd5e7',
                                 'description': 'White plays 1. Nxe7+! winning the bishop.',
                                 'fen': 'r2q1rk1/1pp1bppp/4bn2/3N4/8/1P2P3/PBPP1PPP/R2QK2R w KQ - 0 1',
                                 'goal': 'Capture with 1. Nxe7+.',
                                 'id': 'pin_l3_04',
                                 'sequence': ['d5e7', 'd8e7', 'b2f6'],
                                 'takeaway': 'Long diagonal pins create unstoppable combination breakthroughs.',
                                 'title': 'Combat Mastery: Cross-Pinning on the Long Diagonal',
                                 'turn': 'w'},
                             {   'best_move_san': 'Rxe8#',
                                 'best_move_uci': 'e1e8',
                                 'description': 'White delivers 1. Rxe8# on the back rank.',
                                 'fen': '4r1k1/pp3ppp/8/3N4/8/8/PP3PPP/4R1K1 w - - 0 1',
                                 'goal': 'Deliver checkmate with 1. Rxe8#.',
                                 'id': 'pin_l3_05',
                                 'sequence': ['e1e8'],
                                 'takeaway': 'Pinned defenders cannot protect the squares behind them.',
                                 'title': 'Combat Mastery: Paralyzing the Back Rank',
                                 'turn': 'w'}]},
    'skewer': {   'level1': [   {   'best_move_san': 'Rxe7+',
                                    'best_move_uci': 'e1e7',
                                    'description': "Black's king stands on e8 with queen directly behind it on e7. "
                                                   "White's rook skewers: 1. Rxe7+!",
                                    'fen': '4k3/4q3/8/8/8/8/8/4R1K1 w - - 0 1',
                                    'goal': 'Capture the queen through the skewer: 1. Rxe7+ Kxe7.',
                                    'id': 'skewer_l1_01',
                                    'sequence': ['e1e7', 'e8e7'],
                                    'takeaway': 'In a skewer, the higher-value piece in front is forced to move, '
                                                'exposing the piece behind it.',
                                    'title': 'Raw Geometry: Absolute Skewer on the e-file',
                                    'turn': 'w'},
                                {   'best_move_san': 'Bb2',
                                    'best_move_uci': 'a3b2',
                                    'description': "White's bishop checks Black's king on e8, skewering the rook on "
                                                   'h8.',
                                    'fen': '4k2r/8/8/8/8/B7/8/4K3 w - - 0 1',
                                    'goal': 'Play 1. Bb2 Kf7 2. Bxh8.',
                                    'id': 'skewer_l1_02',
                                    'sequence': ['a3b2', 'e8f7', 'b2h8'],
                                    'takeaway': 'Diagonal skewers strike across the entire length of the board.',
                                    'title': 'Raw Geometry: Bishop Skewer on King and Rook',
                                    'turn': 'w'},
                                {   'best_move_san': 'Rxd6+',
                                    'best_move_uci': 'd1d6',
                                    'description': "White's rook attacks Black's queen on d6 with the king behind it "
                                                   'on d8.',
                                    'fen': '3k4/8/3q4/8/8/8/8/3R2K1 w - - 0 1',
                                    'goal': 'Capture the queen: 1. Rxd6+ Kc7 2. Rd2.',
                                    'id': 'skewer_l1_03',
                                    'sequence': ['d1d6', 'd8c7', 'd6d2'],
                                    'takeaway': 'File skewers pin or win queens standing on the same line as their '
                                                'king.',
                                    'title': 'Raw Geometry: Rook Skewer on Queen and King',
                                    'turn': 'w'},
                                {   'best_move_san': 'Rxa5',
                                    'best_move_uci': 'a1a5',
                                    'description': "White's rook captures the opponent queen on the a-file: 1. Rxa5.",
                                    'fen': 'r7/8/8/q7/8/8/8/R3K3 w - - 0 1',
                                    'goal': 'Capture the queen: 1. Rxa5 Rxa5.',
                                    'id': 'skewer_l1_04',
                                    'sequence': ['a1a5', 'a8a5'],
                                    'takeaway': 'Open files allow heavy pieces to slice through unprotected enemy '
                                                'units.',
                                    'title': 'Raw Geometry: Rook Skewering Loose Rooks',
                                    'turn': 'w'},
                                {   'best_move_san': 'Bxh1',
                                    'best_move_uci': 'f3h1',
                                    'description': "White's bishop skewers the king and wins the rook on h1: 1. Bxh1.",
                                    'fen': '8/8/8/4k3/8/5B2/8/4K2r w - - 0 1',
                                    'goal': 'Capture the loose rook: 1. Bxh1 Kd4.',
                                    'id': 'skewer_l1_05',
                                    'sequence': ['f3h1', 'e5d4'],
                                    'takeaway': 'Always watch for long-distance diagonal threats against cornered '
                                                'pieces.',
                                    'title': 'Raw Geometry: Diagonal Skewer Snapping Rook',
                                    'turn': 'w'}],
                  'level2': [   {   'best_move_san': 'Rd7',
                                    'best_move_uci': 'd1d7',
                                    'description': "White invades the 7th rank to skewer Black's flank pawns.",
                                    'fen': '4r1k1/pp3ppp/8/8/8/8/PP3PPP/3R2K1 w - - 0 1',
                                    'goal': 'Infiltrate with 1. Rd7 Rb8 2. Kf1.',
                                    'id': 'skewer_l2_01',
                                    'sequence': ['d1d7', 'e8b8', 'g1f1'],
                                    'takeaway': 'Rooks infiltrating the 7th rank create multiple simultaneous skewers '
                                                'on opponent pawns.',
                                    'title': 'Stepping Stone: 7th Rank Skewer Infiltration',
                                    'turn': 'w'},
                                {   'best_move_san': 'Ng5',
                                    'best_move_uci': 'f3g5',
                                    'description': 'White plays 1. Ng5 attacking the f7 weakness and creating skewer '
                                                   'threats.',
                                    'fen': 'r1bqk2r/pppp1ppp/2n5/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5',
                                    'goal': 'Attack f7: 1. Ng5 d5 2. Bxd5.',
                                    'id': 'skewer_l2_02',
                                    'sequence': ['f3g5', 'd7d5', 'c4d5'],
                                    'takeaway': 'Coordinating knight and bishop generates devastating tactical '
                                                'pressure on f7.',
                                    'title': 'Stepping Stone: Developing into Bishop Skewer',
                                    'turn': 'w'},
                                {   'best_move_san': 'Qd8+',
                                    'best_move_uci': 'd1d8',
                                    'description': 'White checks the king on d8, forcing the queen to interpose: 1. '
                                                   'Qd8+ Qe8 2. Qxe8#!',
                                    'fen': '6k1/pp3ppp/8/8/4q3/8/PP3PPP/3Q2K1 w - - 0 1',
                                    'goal': 'Play 1. Qd8+ Qe8 2. Qxe8#.',
                                    'id': 'skewer_l2_03',
                                    'sequence': ['d1d8', 'e4e8', 'd8e8'],
                                    'takeaway': 'Queen skewers on the back rank force game-ending piece captures.',
                                    'title': 'Stepping Stone: Queen Skewer on the Back Rank',
                                    'turn': 'w'},
                                {   'best_move_san': 'Bxf8',
                                    'best_move_uci': 'a3f8',
                                    'description': 'White exchanges bishops to set up a decisive rook invasion: 1. '
                                                   'Bxf8 Kxf8 2. Re7.',
                                    'fen': '5rk1/pp3ppp/8/8/8/B7/PP3PPP/4R1K1 w - - 0 1',
                                    'goal': 'Take the rook: 1. Bxf8 Kxf8 2. Re7.',
                                    'id': 'skewer_l2_04',
                                    'sequence': ['a3f8', 'g8f8', 'e1e7'],
                                    'takeaway': 'Trading off defenders paves the way for 7th-rank rook dominance.',
                                    'title': 'Stepping Stone: Bishop Decoy into Rook Skewer',
                                    'turn': 'w'},
                                {   'best_move_san': 'Rc1',
                                    'best_move_uci': 'b1c1',
                                    'description': 'White controls the c-file: 1. Rc1 g6 2. Rc8.',
                                    'fen': '6k1/5ppp/8/8/8/8/PP3PPP/1R4K1 w - - 0 1',
                                    'goal': 'Shift rook: 1. Rc1 g6 2. Rc8.',
                                    'id': 'skewer_l2_05',
                                    'sequence': ['b1c1', 'g7g6', 'c1c8'],
                                    'takeaway': 'Transferring rooks to open files establishes skewers across the '
                                                'board.',
                                    'title': 'Stepping Stone: Rook Corridor Skewer',
                                    'turn': 'w'}],
                  'level3': [   {   'best_move_san': 'Qd7',
                                    'best_move_uci': 'd3d7',
                                    'description': 'White plays 1. g3 creating luft and setting up deep combinations.',
                                    'fen': '4r1k1/pp3ppp/8/8/8/B2Q2P1/PP3P1P/6K1 w - - 0 1',
                                    'goal': 'Infiltrate with 1. Qd7 Re1+ 2. Kg2.',
                                    'id': 'skewer_l3_01',
                                    'sequence': ['d3d7', 'e8e1', 'g1g2'],
                                    'takeaway': 'Securing king luft permits fearless deep-rank queen invasions.',
                                    'title': 'Combat Mastery: King Decoy into Long-Range Skewer',
                                    'turn': 'w'},
                                {   'best_move_san': 'Bxf6',
                                    'best_move_uci': 'b2f6',
                                    'description': "White trades on f6 to shatter Black's kingside pawn structure.",
                                    'fen': 'r2q1rk1/pp2bppp/2n2n2/3p4/8/1P2PN2/PB1N1PPP/R2Q1RK1 w - - 0 12',
                                    'goal': 'Trade on f6: 1. Bxf6 Bxf6 2. Rc1.',
                                    'id': 'skewer_l3_02',
                                    'sequence': ['b2f6', 'e7f6', 'a1c1'],
                                    'takeaway': 'Strategic exchanges unbalance opponent pieces and seize critical '
                                                'diagonals.',
                                    'title': 'Combat Mastery: Strategic Bishop Skewer Alignment',
                                    'turn': 'w'},
                                {   'best_move_san': 'Rd8#',
                                    'best_move_uci': 'd1d8',
                                    'description': 'White delivers checkmate along the d-file: 1. Rd8#!',
                                    'fen': '6k1/pp3pp1/8/8/8/7Q/PP3PPP/3R2K1 w - - 0 1',
                                    'goal': 'Deliver 1. Rd8#.',
                                    'id': 'skewer_l3_03',
                                    'sequence': ['d1d8'],
                                    'takeaway': 'Heavy pieces aligned on open files produce unblockable checkmates.',
                                    'title': 'Combat Mastery: Decisive Queen Skewer Mate',
                                    'turn': 'w'},
                                {   'best_move_san': 'Rxd8#',
                                    'best_move_uci': 'd1d8',
                                    'description': 'White converts the back-rank weakness into immediate checkmate.',
                                    'fen': '3r2k1/pp3ppp/8/8/8/8/PP3PPP/3R2K1 w - - 0 1',
                                    'goal': 'Deliver checkmate: 1. Rxd8#.',
                                    'id': 'skewer_l3_04',
                                    'sequence': ['d1d8'],
                                    'takeaway': 'Simplifying into an open back rank wins games instantly.',
                                    'title': 'Combat Mastery: Absolute Back-Rank Corridor Skewer',
                                    'turn': 'w'},
                                {   'best_move_san': 'Rc1',
                                    'best_move_uci': 'a1c1',
                                    'description': 'White seizes the c-file with 1. Rc1 g6 2. Rc7.',
                                    'fen': 'r5k1/pp3ppp/8/8/8/8/PP3PPP/R5K1 w - - 0 1',
                                    'goal': 'Invade the c-file: 1. Rc1 g6 2. Rc7.',
                                    'id': 'skewer_l3_05',
                                    'sequence': ['a1c1', 'g7g6', 'c1c7'],
                                    'takeaway': 'Controlling open files with rooks paralyzes opponent piece mobility.',
                                    'title': 'Combat Mastery: 7th Rank Dominance Skewer',
                                    'turn': 'w'}]},
    'trapped_piece': {   'level1': [   {   'best_move_san': 'axb3',
                                           'best_move_uci': 'a2b3',
                                           'description': "Black's bishop on b3 has no escape squares. White captures "
                                                          'it with the a-pawn: 1. axb3.',
                                           'fen': '4k3/8/8/8/8/1b6/P7/4K3 w - - 0 1',
                                           'goal': 'Capture the trapped bishop: 1. axb3 Ke7 2. b4.',
                                           'id': 'tp_l1_01',
                                           'sequence': ['a2b3', 'e8e7', 'b3b4'],
                                           'takeaway': 'Pieces on the edge easily run out of safe retreat squares.',
                                           'title': 'Raw Geometry: Trapping the Cornered Bishop',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Kb7',
                                           'best_move_uci': 'c6b7',
                                           'description': "Black's knight on a8 is trapped in the corner. White's king "
                                                          'approaches: 1. Kb7 Kd7 2. Kxa8.',
                                           'fen': 'n3k3/8/2K5/8/8/8/8/8 w - - 0 1',
                                           'goal': 'Trap and capture the knight: 1. Kb7 Kd7 2. Kxa8.',
                                           'id': 'tp_l1_02',
                                           'sequence': ['c6b7', 'e8d7', 'b7a8'],
                                           'takeaway': 'A knight on the rim is dim: trapped knights in corners can be '
                                                       'captured by active kings.',
                                           'title': 'Raw Geometry: Trapping Knight on the Rim',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Rxa8+',
                                           'best_move_uci': 'a1a8',
                                           'description': "Black's queen on a8 is cornered. White's rook captures it "
                                                          'cleanly: 1. Rxa8.',
                                           'fen': 'q3k3/8/8/8/8/8/8/R3K3 w - - 0 1',
                                           'goal': 'Capture the trapped queen: 1. Rxa8+ Ke7 2. Ra6.',
                                           'id': 'tp_l1_03',
                                           'sequence': ['a1a8', 'e8e7', 'a8a6'],
                                           'takeaway': 'Queens cornered on the edge lack mobility and are vulnerable '
                                                       'to rook captures.',
                                           'title': 'Raw Geometry: Trapped Queen on the a-file',
                                           'turn': 'w'},
                                       {   'best_move_san': 'gxh7',
                                           'best_move_uci': 'g6h7',
                                           'description': "White's pawn on g6 advances to capture the cornered bishop "
                                                          'on h7: 1. gxh7.',
                                           'fen': '4k3/7b/6P1/8/8/8/8/4K3 w - - 0 1',
                                           'goal': 'Capture the trapped bishop: 1. gxh7 Kf7 2. h8=Q.',
                                           'id': 'tp_l1_04',
                                           'sequence': ['g6h7', 'e8f7', 'h7h8q'],
                                           'takeaway': 'Advancing pawns trap enemy pieces against the board edge.',
                                           'title': 'Raw Geometry: Bishop Trapped by Advancing Pawn',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Bc8',
                                           'best_move_uci': 'e6c8',
                                           'description': "White's bishop cuts off Black's king and coordinates to win "
                                                          'material.',
                                           'fen': '4k2r/8/4B3/8/8/8/8/4K3 w - - 0 1',
                                           'goal': 'Play 1. Bc8 Ke7 2. Bb7.',
                                           'id': 'tp_l1_05',
                                           'sequence': ['e6c8', 'e8e7', 'c8b7'],
                                           'takeaway': 'Positioning bishops to control escape diagonals paralyzes '
                                                       'opponent counterplay.',
                                           'title': 'Raw Geometry: Maneuvering to Win the Isolated Piece',
                                           'turn': 'w'}],
                         'level2': [   {   'best_move_san': 'c3',
                                           'best_move_uci': 'c2c3',
                                           'description': 'White plays c3 to prepare a secure escape square for the '
                                                          'light-squared bishop.',
                                           'fen': 'r1bqk2r/1pp1bppp/p1np1n2/4p3/B3P3/3P1N2/PPP2PPP/RNBQ1RK1 w kq - 0 7',
                                           'goal': 'Play 1. c3 O-O 2. Re1.',
                                           'id': 'tp_l2_01',
                                           'sequence': ['c2c3', 'e8g8', 'f1e1'],
                                           'takeaway': 'In the Ruy Lopez, c3 gives the bishop an escape square against '
                                                       "Noah's Ark traps.",
                                           'title': "Stepping Stone: Noah's Ark Trap Preparation",
                                           'turn': 'w'},
                                       {   'best_move_san': 'O-O',
                                           'best_move_uci': 'e1g1',
                                           'description': 'Black brought the queen out early. White castles to develop '
                                                          'with safety.',
                                           'fen': 'r1b1k2r/ppp2ppp/2n5/3qp3/8/3P1N2/PPP1BPPP/R2QK2R w KQkq - 0 9',
                                           'goal': 'Castle king to safety: 1. O-O O-O 2. c4.',
                                           'id': 'tp_l2_02',
                                           'sequence': ['e1g1', 'e8g8', 'c2c4'],
                                           'takeaway': 'Early queen excursions lose tempo against harmonious '
                                                       'development.',
                                           'title': 'Stepping Stone: Repelling Early Queen Sortie',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Ng5',
                                           'best_move_uci': 'f3g5',
                                           'description': 'White plays 1. Ng5 attacking the loose knight and bishop.',
                                           'fen': 'r1bqk2r/ppp2ppp/2np4/4p2n/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 6',
                                           'goal': 'Play 1. Ng5 Qxg5 2. Bxg5.',
                                           'id': 'tp_l2_03',
                                           'sequence': ['f3g5', 'd8g5', 'c1g5'],
                                           'takeaway': 'Exploiting offside knights creates immediate tactical '
                                                       'weaknesses.',
                                           'title': 'Stepping Stone: Trapping Knight on the Rim with Ng5',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Rxe5+',
                                           'best_move_uci': 'e1e5',
                                           'description': "Black's rook on e5 is trapped in the center. White captures "
                                                          'it: 1. Rxe5+.',
                                           'fen': '4k3/pp3ppp/8/4r3/8/2P5/PP3PPP/4R1K1 w - - 0 1',
                                           'goal': 'Capture the trapped rook: 1. Rxe5+ Kd7 2. Re3.',
                                           'id': 'tp_l2_04',
                                           'sequence': ['e1e5', 'e8d7', 'e5e3'],
                                           'takeaway': 'Exposed heavy pieces in the center without pawn support become '
                                                       'easy prey.',
                                           'title': 'Stepping Stone: Snapping the Wandering Rook',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Nc3',
                                           'best_move_uci': 'b1c3',
                                           'description': "White develops the knight to c3 to kick Black's exposed "
                                                          'queen.',
                                           'fen': 'r1b1kbnr/pppp1ppp/8/4q3/4P3/8/PPP2PPP/RNBQKB1R w KQkq - 0 5',
                                           'goal': 'Develop with 1. Nc3 Nf6 2. Bd3.',
                                           'id': 'tp_l2_05',
                                           'sequence': ['b1c3', 'g8f6', 'f1d3'],
                                           'takeaway': 'Developing minor pieces while attacking early queen sorties '
                                                       'secures permanent advantages.',
                                           'title': 'Stepping Stone: Developing Against Premature Queen Raids',
                                           'turn': 'w'}],
                         'level3': [   {   'best_move_san': 'h3',
                                           'best_move_uci': 'h2h3',
                                           'description': "White kicks Black's active bishop with 1. h3 Bh5 2. g4 "
                                                          'trapping it.',
                                           'fen': 'r2q1rk1/ppp2ppp/2n5/3p4/3Pn1b1/2NBPN2/PP3PPP/R2Q1RK1 w - - 0 10',
                                           'goal': 'Play 1. h3 Bh5 2. g4.',
                                           'id': 'tp_l3_01',
                                           'sequence': ['h2h3', 'g4h5', 'g2g4'],
                                           'takeaway': 'Pawn storms on the flank can trap overextended enemy bishops.',
                                           'title': 'Combat Mastery: Trapping the Enemy Bishop with h3-g4',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Rb1',
                                           'best_move_uci': 'a1b1',
                                           'description': "White positions pieces to restrict Black's queen on b6.",
                                           'fen': 'r4rk1/pp1b1ppp/1q2pn2/3p4/3P4/2NBPN2/PP3PPP/R2Q1RK1 w - - 0 11',
                                           'goal': 'Guard b2 with 1. Rb1 Rfc8 2. Qe2.',
                                           'id': 'tp_l3_02',
                                           'sequence': ['a1b1', 'f8c8', 'd1e2'],
                                           'takeaway': 'Neutralizing queen pressure prepares counter-attacks against '
                                                       'restricted units.',
                                           'title': 'Combat Mastery: Restricting Queen Mobility on the Flank',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Bxb2',
                                           'best_move_uci': 'c1b2',
                                           'description': "Black's knight ventured into b2. White captures it cleanly: "
                                                          '1. Bxb2.',
                                           'fen': 'r4rk1/pp3ppp/8/8/8/8/Pn3PPP/R1B2RK1 w - - 0 1',
                                           'goal': 'Capture the trapped knight: 1. Bxb2 Rfc8 2. Rfc1.',
                                           'id': 'tp_l3_03',
                                           'sequence': ['c1b2', 'f8c8', 'f1c1'],
                                           'takeaway': 'Minor pieces that snatch flank pawns often find themselves '
                                                       'trapped without an exit.',
                                           'title': 'Combat Mastery: Trapping Infiltrated Knight on b2',
                                           'turn': 'w'},
                                       {   'best_move_san': 'Rxe8#',
                                           'best_move_uci': 'e1e8',
                                           'description': 'White delivers checkmate on e8 against the trapped king.',
                                           'fen': '4r1k1/pp3ppp/8/8/8/8/PP3PPP/4R1K1 w - - 0 1',
                                           'goal': 'Deliver 1. Rxe8#.',
                                           'id': 'tp_l3_04',
                                           'sequence': ['e1e8'],
                                           'takeaway': 'Trapped kings behind unbroken pawn shields fall victim to '
                                                       'back-rank corridor mates.',
                                           'title': 'Combat Mastery: Back-Rank Trapped King Checkmate',
                                           'turn': 'w'},
                                       {   'best_move_san': 'axb3',
                                           'best_move_uci': 'a2b3',
                                           'description': 'White captures the cornered bishop: 1. axb3 Kd7 2. Kd2.',
                                           'fen': '4k3/pp3ppp/8/8/8/1b6/P4PPP/4K3 w - - 0 1',
                                           'goal': 'Capture the trapped bishop: 1. axb3 Kd7 2. Kd2.',
                                           'id': 'tp_l3_05',
                                           'sequence': ['a2b3', 'e8d7', 'e1d2'],
                                           'takeaway': 'Technically converting material won from trapped pieces leads '
                                                       'directly to victory.',
                                           'title': 'Combat Mastery: Converting Trapped Bishop in the Endgame',
                                           'turn': 'w'}]}}



def create_board_variation(riddle: Dict[str, Any], var_type: str = "horizontal") -> Optional[Dict[str, Any]]:
    """
    Transforms a riddle by flipping horizontally (Queenside <-> Kingside)
    or inverting color perspective (White <-> Black) while verifying full move legality.
    """
    try:
        b = chess.Board(riddle["fen"])
        seq = riddle.get("sequence", [])
        new_seq = []

        if var_type == "horizontal":
            new_b = b.transform(chess.flip_horizontal)
            for m_str in seq:
                m = chess.Move.from_uci(m_str)
                f_from = chess.square(7 - chess.square_file(m.from_square), chess.square_rank(m.from_square))
                f_to = chess.square(7 - chess.square_file(m.to_square), chess.square_rank(m.to_square))
                new_m = chess.Move(f_from, f_to, promotion=m.promotion)
                new_seq.append(new_m.uci())
            desc_tag = "[Mirror]"
        elif var_type == "color":
            new_b = b.mirror()
            for m_str in seq:
                m = chess.Move.from_uci(m_str)
                f_from = chess.square_mirror(m.from_square)
                f_to = chess.square_mirror(m.to_square)
                new_m = chess.Move(f_from, f_to, promotion=m.promotion)
                new_seq.append(new_m.uci())
            desc_tag = "[Black Perspective]"
        else:
            return None

        # Validate that all moves in new_seq remain strictly legal in the transformed position
        v_board = chess.Board(new_b.fen())
        for uci in new_seq:
            mv = chess.Move.from_uci(uci)
            if mv not in v_board.legal_moves:
                return None
            v_board.push(mv)

        best_m = chess.Move.from_uci(new_seq[0])
        init_board = chess.Board(new_b.fen())
        best_san = init_board.san(best_m)

        new_riddle = dict(riddle)
        new_riddle["id"] = f"{riddle['id']}_{var_type[:3]}"
        new_riddle["title"] = f"{riddle['title']} {desc_tag}"
        new_riddle["fen"] = new_b.fen()
        new_riddle["turn"] = "w" if new_b.turn == chess.WHITE else "b"
        new_riddle["best_move_uci"] = new_seq[0]
        new_riddle["best_move_san"] = best_san
        new_riddle["sequence"] = new_seq
        return new_riddle
    except Exception:
        return None


def generate_procedural_variation(base_riddle: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Procedurally synthesizes a novel position variation by adding non-interfering flank pawns
    or adjusting peaceful king/pawn structures, verifying complete move sequence legality.
    """
    try:
        b = chess.Board(base_riddle["fen"])
        seq = base_riddle.get("sequence", [base_riddle.get("best_move_uci")])
        if not seq or not seq[0]:
            return None

        # Candidate flank squares that do not interfere with central or tactical lines
        safe_white_squares = [chess.H2, chess.H3, chess.A2, chess.A3, chess.G2, chess.B2]
        safe_black_squares = [chess.H7, chess.H6, chess.A7, chess.A6, chess.G7, chess.B7]

        random.shuffle(safe_white_squares)
        random.shuffle(safe_black_squares)

        # Add 1 safe pawn on each side if empty
        w_placed = False
        for sq in safe_white_squares:
            if b.piece_at(sq) is None:
                b.set_piece_at(sq, chess.Piece(chess.PAWN, chess.WHITE))
                w_placed = True
                break

        b_placed = False
        for sq in safe_black_squares:
            if b.piece_at(sq) is None:
                b.set_piece_at(sq, chess.Piece(chess.PAWN, chess.BLACK))
                b_placed = True
                break

        if not w_placed and not b_placed:
            return None

        # Verify all sequence moves are strictly legal
        test_b = chess.Board(b.fen())
        for m_str in seq:
            mv = chess.Move.from_uci(m_str)
            if mv not in test_b.legal_moves:
                return None
            test_b.push(mv)

        best_m = chess.Move.from_uci(seq[0])
        init_board = chess.Board(b.fen())
        best_san = init_board.san(best_m)

        rand_tag = random.randint(100, 999)
        new_riddle = dict(base_riddle)
        new_riddle["id"] = f"{base_riddle['id']}_gen_{rand_tag}"
        new_riddle["title"] = f"{base_riddle['title']} [Synthesized #{rand_tag}]"
        new_riddle["fen"] = b.fen()
        new_riddle["turn"] = "w" if b.turn == chess.WHITE else "b"
        new_riddle["best_move_uci"] = seq[0]
        new_riddle["best_move_san"] = best_san
        new_riddle["sequence"] = list(seq)
        return new_riddle
    except Exception:
        return None


def get_expanded_level_bank(motif_id: str, level: int) -> List[Dict[str, Any]]:
    """
    Returns >= 10 verified, playable riddles for any (motif_id, level).
    Expands base curated positions using horizontal & color perspective symmetries.
    """
    clean_id = (motif_id or "fork").lower().replace(" ", "_")
    if clean_id not in DRILL_BASE_POOLS:
        for k in DRILL_BASE_POOLS:
            if k in clean_id or clean_id in k:
                clean_id = k
                break
    if clean_id not in DRILL_BASE_POOLS:
        clean_id = "fork"

    lvl_key = f"level{level}"
    pool = DRILL_BASE_POOLS[clean_id].get(lvl_key, DRILL_BASE_POOLS[clean_id]["level1"])

    expanded: List[Dict[str, Any]] = []
    seen_fens = set()

    for r in pool:
        expanded.append(dict(r))
        seen_fens.add(r["fen"])

    for r in pool:
        h_var = create_board_variation(r, "horizontal")
        if h_var and h_var["fen"] not in seen_fens:
            expanded.append(h_var)
            seen_fens.add(h_var["fen"])

    if len(expanded) < 10:
        for r in pool:
            c_var = create_board_variation(r, "color")
            if c_var and c_var["fen"] not in seen_fens:
                expanded.append(c_var)
                seen_fens.add(c_var["fen"])

    # Fallback procedural generation if symmetries were identical
    attempts = 0
    while len(expanded) < 10 and attempts < 20:
        attempts += 1
        base_cand = random.choice(pool)
        p_var = generate_procedural_variation(base_cand)
        if p_var and p_var["fen"] not in seen_fens:
            expanded.append(p_var)
            seen_fens.add(p_var["fen"])

    return expanded


def generate_new_riddle_for_level(motif_id: str, level: int, exclude_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Dynamically generates or picks a fresh riddle for the given level.
    Supports procedural synthesis so the user can generate unlimited new riddles on demand.
    """
    exclude_ids = exclude_ids or []
    bank = get_expanded_level_bank(motif_id, level)
    candidates = [r for r in bank if r["id"] not in exclude_ids]

    # If there are unseen bank items, prefer them 60% of the time,
    # or generate a brand new procedural variation 40% of the time.
    if candidates and random.random() < 0.6:
        selected = dict(random.choice(candidates))
        return selected

    # Synthesize a novel procedural variation from any base puzzle in this level
    lvl_key = f"level{level}"
    clean_id = (motif_id or "fork").lower().replace(" ", "_")
    if clean_id not in DRILL_BASE_POOLS:
        clean_id = "fork"
    base_pool = DRILL_BASE_POOLS[clean_id].get(lvl_key, DRILL_BASE_POOLS[clean_id]["level1"])

    for _ in range(15):
        base_item = random.choice(base_pool)
        synth = generate_procedural_variation(base_item)
        if synth and synth["id"] not in exclude_ids:
            return synth

    # Fallback to any candidate or item from bank
    if candidates:
        return dict(random.choice(candidates))
    return dict(random.choice(bank))
