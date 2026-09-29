import unittest
import json
import sys
import chess
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.main import (
    app, USER_PROFILES, ACTIVE_PROFILE_ID, USER_SKILLS,
    CONVERT_SYSTEMS, PLACEMENT_QUESTIONS,
    classify_move, generate_post_game_summary
)
from fastapi.testclient import TestClient

client = TestClient(app)

class TestChessBookLM(unittest.TestCase):

    def test_health_check(self):
        response = client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)

    def test_user_profiles_endpoints(self):
        # 1. Get profiles
        res = client.get("/api/user/profiles")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("profiles", data)
        self.assertIn("active_profile_id", data)

        # 2. Create new profile
        create_res = client.post("/api/user/profiles", json={"name": "Test Grandmaster", "starting_elo": 1800})
        self.assertEqual(create_res.status_code, 200)
        created_data = create_res.json()
        new_id = created_data["profile"]["id"]
        self.assertEqual(created_data["profile"]["name"], "Test Grandmaster")
        self.assertEqual(created_data["profile"]["estimated_elo"], 1800)

        # 3. Switch to new profile
        switch_res = client.post("/api/user/profiles/switch", json={"profile_id": new_id})
        self.assertEqual(switch_res.status_code, 200)

        # 4. Active profile check
        active_res = client.get("/api/user/active-profile")
        self.assertEqual(active_res.status_code, 200)
        self.assertEqual(active_res.json()["profile"]["id"], new_id)

    def test_skill_matrix_and_conversions(self):
        res = client.get("/api/user/skills")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("skills", data)
        self.assertIn("rating_conversions", data)
        self.assertTrue(len(data["skills"]) >= 6)

    def test_placement_test(self):
        # Get questions
        q_res = client.get("/api/user/placement-test")
        self.assertEqual(q_res.status_code, 200)
        questions = q_res.json()["questions"]
        self.assertTrue(len(questions) >= 3)

        # Submit answers
        answers = {q["id"]: q["options"][0]["tier_score"] for q in questions}
        sub_res = client.post("/api/user/placement-test/submit", json={"answers": answers})
        self.assertEqual(sub_res.status_code, 200)
        res_data = sub_res.json()
        self.assertIn("assigned_elo", res_data)
        self.assertIn("assessment", res_data)

    def test_game_analysis_endpoint(self):
        moves = ["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5"]
        res = client.post("/api/game/analyze", json={"moves": moves})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("white_accuracy", data)
        self.assertIn("black_accuracy", data)
        self.assertIn("move_evals", data)
        self.assertIn("coach_report", data)

    def test_classify_move_logic(self):
        # Brilliant move check (tactical sacrificial gain)
        cls_brilliant, text_b = classify_move(best_eval_cp=100, actual_eval_cp=450, cp_diff=-350, is_white=True)
        self.assertEqual(cls_brilliant, "brilliant")

        # Best move check
        cls_best, text_best = classify_move(best_eval_cp=100, actual_eval_cp=105, cp_diff=-5, is_white=True)
        self.assertEqual(cls_best, "best")

        # Blunder check
        cls_blunder, text_blunder = classify_move(best_eval_cp=200, actual_eval_cp=-150, cp_diff=350, is_white=True)
        self.assertEqual(cls_blunder, "blunder")

    def test_bot_move_target_elo(self):
        res = client.post("/api/board/bot-move", json={"moves": ["e4"], "skill_level": 4, "target_elo": 1350})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("move_uci", data)
        self.assertIn("move_san", data)
        self.assertEqual(data["target_elo"], 1350)

    def test_live_coaching_endpoint(self):
        res = client.post("/api/mentor/live-coaching", json={
            "moves": ["e4", "e5"],
            "move_number": 2,
            "student_color": "white",
            "practice_subject": "loose_pieces"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["move_number"], 2)
        self.assertIn("response", data)

    def test_board_overlays_endpoint(self):
        moves = ["e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6", "Be2", "e5", "Nf3", "Be7"]
        res = client.post("/api/board/overlays", json={"moves": moves})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertIn("overlays", data)
        self.assertIsInstance(data["overlays"], list)
        self.assertTrue(len(data["overlays"]) > 0)
        
        # Verify overlay keys
        first_overlay = data["overlays"][0]
        self.assertIn("square", first_overlay)
        self.assertIn("side", first_overlay)
        self.assertIn("type", first_overlay)
        self.assertIn("badge", first_overlay)
        self.assertIn("tooltip", first_overlay)

    def test_knight_attacked_by_pawn_target_overlay(self):
        # 1. e4 Nf6 2. e5
        moves = ["e4", "Nf6", "e5"]
        res = client.post("/api/board/overlays", json={"moves": moves})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        f6_overlays = [o for o in data.get("overlays", []) if o.get("square") == "f6"]
        self.assertTrue(len(f6_overlays) > 0, "Square f6 should be marked as target overlay when knight is attacked by e5 pawn")
        self.assertEqual(f6_overlays[0]["category"], "weak")
        self.assertEqual(f6_overlays[0]["type"], "target")

    def test_llm_square_analysis_endpoint(self):
        moves = ["e4", "Nf6", "e5"]
        res = client.post("/api/board/llm-square-analysis", json={"moves": moves})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertIn("overlays", data)
        self.assertIn("response", data)
        self.assertIsInstance(data["overlays"], list)
        self.assertTrue(len(data["overlays"]) > 0)

    def test_board_request_builder_accuracy(self):
        # 1. e4 c5 2. Nf3 d6 3. d4 Nf6 4. Nc3 cxd4 5. Nxd4 a6 6. Be2 e5 7. Nf3 Be7
        moves = ["e4", "c5", "Nf3", "d6", "d4", "Nf6", "Nc3", "cxd4", "Nxd4", "a6", "Be2", "e5", "Nf3", "Be7"]
        from backend.main import build_board_from_request
        board = build_board_from_request(None, moves)
        
        # Verify knight is at f3 (square 21 in python-chess, f3 = 21)
        self.assertEqual(board.piece_at(chess.F3).symbol(), 'N')
        # Verify d4 is empty (not occupied by knight)
        self.assertIsNone(board.piece_at(chess.D4))

if __name__ == "__main__":
    unittest.main()

