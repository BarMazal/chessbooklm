import sys
import unittest
from pathlib import Path

import chess

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient

from backend.main import app, engine_manager
from backend.move_analysis import analyze_move, build_sequence_analysis

client = TestClient(app)
HAS_ENGINE = engine_manager._engine is not None


def ev(cp=None, mate=None, best=None):
    return {"cp": cp, "mate": mate, "best_move": best, "depth": 14, "source": "test"}


class TestMotifDetection(unittest.TestCase):
    """Board-pattern detection with fixed (fake) engine numbers, so these run without Stockfish."""

    def motif_ids(self, motifs):
        return [m["id"] for m in motifs]

    def test_e4_is_book_and_has_no_forced_patterns(self):
        r = analyze_move(chess.STARTING_FEN, "e2e4", 1, ev(30, best="e2e4"), ev(30), ["e2e4"])
        self.assertEqual(r["engine"]["quality"], "Book")
        self.assertEqual(r["move"]["category"], "book")
        self.assertEqual(r["move"]["motifs_against"], [])  # no back-rank / exposed-king noise
        self.assertIsNone(r["move"]["primary_motif"])
        self.assertIsNone(r["context"]["opening"]["name"])  # no opening named from future moves

    def test_opening_named_only_from_played_moves(self):
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
        r = analyze_move(fen, "e7e6", 1, ev(30, best="c7c5"), ev(40), ["e2e4", "e7e6"])
        self.assertEqual(r["context"]["opening"]["name"], "French Defense")

    def test_knight_fork_is_primary_motif_for_mover(self):
        fen = "r3k3/pp3ppp/8/1N6/8/8/PPP2PPP/4K2R w K - 0 20"
        r = analyze_move(fen, "b5c7", 20, ev(800, best="b5c7"), ev(800))
        self.assertEqual(r["move"]["primary_motif"]["id"], "fork")
        self.assertEqual(r["move"]["primary_motif"]["side"], "for")
        self.assertEqual(r["move"]["category"], "tactical")

    def test_discovered_check_only_from_revealed_slider(self):
        fen = "4k3/8/8/8/4N3/8/8/4R1K1 w - - 0 30"
        r = analyze_move(fen, "e4c5", 30, ev(450, best="e4d6"), ev(450))
        self.assertIn("discovered_attack", self.motif_ids(r["move"]["motifs_for"]))
        # A slider that merely moves and attacks something is not a discovered attack
        r2 = analyze_move("4k3/8/8/8/8/8/8/R5K1 w - - 0 30", "a1a8", 30, ev(900, best="a1a8"), ev(900))
        self.assertNotIn("discovered_attack", self.motif_ids(r2["move"]["motifs_for"]))

    def test_hanging_piece_blunder_is_against_mover(self):
        fen = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
        r = analyze_move(fen, "f3g5", 3, ev(37, best="f1b5"), ev(-740))
        self.assertEqual(r["engine"]["quality"], "Blunder")
        self.assertEqual(r["move"]["primary_motif"]["id"], "hanging_piece")
        self.assertEqual(r["move"]["primary_motif"]["side"], "against")
        self.assertGreater(r["move"]["aspects"]["opponent_score"], 50)

    def test_back_rank_only_when_the_move_allows_it(self):
        fen = "2r3k1/5ppp/8/8/8/8/5PPP/4R1K1 b - - 0 30"
        r = analyze_move(fen, "c8c2", 30, ev(0, best="h7h6"), ev(mate=1))
        self.assertIn("back_rank", self.motif_ids(r["move"]["motifs_against"]))

    def test_back_rank_check_that_wins_material(self):
        fen = "4r1k1/5ppp/3n4/8/8/8/5PPP/4R1K1 w - - 0 30"
        r = analyze_move(fen, "e1e8", 30, ev(0, best="e1e8"), ev(0))
        br = [m for m in r["move"]["motifs_for"] if m["id"] == "back_rank"]
        self.assertTrue(br and br[0]["score"] >= 55, r["move"]["motifs_for"])

    def test_missed_mate_is_not_good(self):
        fen = "6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 30"
        r = analyze_move(fen, "g2g3", 30, ev(mate=1, best="e1e8"), ev(670))
        self.assertIn(r["engine"]["quality"], ("Inaccuracy", "Mistake"))
        self.assertTrue(r["engine"]["missed_mate"])

    def test_no_engine_means_null_engine_fields(self):
        r = analyze_move(chess.STARTING_FEN, "g1f3", 1, None, None)
        self.assertIsNone(r["engine"])
        self.assertIsNone(r["move"]["aspects"]["opponent_score"])

    def test_sequence_aggregates_window(self):
        b = chess.Board()
        plies = []
        for uci, cp_b, cp_a in [("e2e4", 30, 30), ("e7e5", 30, 35), ("g1f3", 35, 35), ("b8c6", 35, 40)]:
            plies.append(analyze_move(b.fen(), uci, b.fullmove_number, ev(cp_b, best=uci), ev(cp_a)))
            b.push_uci(uci)
        seq = build_sequence_analysis("b", plies)
        self.assertEqual(seq["window_plies"], 4)
        self.assertEqual(seq["moves"], ["e4", "e5", "Nf3", "Nc6"])
        self.assertEqual(seq["eval_trend"], "steady")


@unittest.skipUnless(HAS_ENGINE, "local Stockfish not available")
class TestAnalysisEndpoints(unittest.TestCase):

    def test_move_endpoint_replays_path(self):
        res = client.post("/api/analysis/move", json={"uci_path": ["e2e4", "e7e5", "g1f3"], "move_number": 2})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        a = data["analysis"]
        self.assertEqual(a["context"]["move_san"], "Nf3")
        self.assertEqual(a["engine"]["source"], "local_stockfish")
        self.assertIsNotNone(a["engine"]["best_move_uci"])

    def test_move_endpoint_rejects_broken_chain(self):
        res = client.post("/api/analysis/move", json={"uci_path": ["e2e4", "d2d4"], "move_number": 2})
        self.assertEqual(res.status_code, 400)

    def test_move_endpoint_rejects_fen_mismatch(self):
        res = client.post("/api/analysis/move", json={"uci_path": ["e2e4"], "move_number": 1,
                                                      "expected_fen_after": chess.STARTING_FEN})
        self.assertEqual(res.status_code, 400)

    def test_mentor_requires_engine_and_never_fakes(self):
        res = client.post("/api/mentor/node-analysis", json={"analysis": {"context": {}, "move": {}}})
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
