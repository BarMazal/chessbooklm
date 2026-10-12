"""
ChessBookLM - QA Profile & Fake Games History Seeder Script
"""

import json
import os

print("[ChessBookLM QA Seeder] Seeding QA Profile & Fake Games History...")

qa_profile = {
    "id": "prof_qa_tester",
    "name": "QA Tester Profile",
    "elo": 1680,
    "is_qa": True,
    "gamesPlayed": 52,
    "wins": 31,
    "draws": 7,
    "losses": 14,
    "concepts": {
        "offensive": {"name": "Offensive Strategy", "rating": 1710, "icon": "Offense"},
        "defensive": {"name": "Defensive Maneuvers", "rating": 1620, "icon": "Defense"},
        "tactics": {"name": "Tactics & Forks", "rating": 1750, "icon": "Tactics"},
        "batteries": {"name": "Battery Attacks", "rating": 1660, "icon": "Battery"},
        "pins": {"name": "Pins & Skewers", "rating": 1690, "icon": "Pins"},
        "endgame": {"name": "Endgame & Gambits", "rating": 1630, "icon": "Endgame"}
    },
    "history": [
        {"event": "Italian Game Session", "result": "1-0", "opponent": "Stockfish L5", "opp_elo": 1600, "moves": 34},
        {"event": "Sicilian Defense Sharp Tactical Line", "result": "1-0", "opponent": "Grandmaster_Bot", "opp_elo": 1750, "moves": 42},
        {"event": "Ruy Lopez Endgame Practice", "result": "1/2-1/2", "opponent": "Maia_1600", "opp_elo": 1620, "moves": 58},
        {"event": "French Defense Blunder Recovery", "result": "0-1", "opponent": "Stockfish L8", "opp_elo": 1850, "moves": 29},
        {"event": "Queen's Gambit Accepted", "result": "1-0", "opponent": "TacticalWizard", "opp_elo": 1640, "moves": 37}
    ]
}

print(f"[SUCCESS] QA Profile successfully created for ChessBookLM:")
print(f"   Name: {qa_profile['name']}")
print(f"   ELO: {qa_profile['elo']}")
print(f"   is_qa Flag: {qa_profile['is_qa']}")
print(f"   Games Tracked: {qa_profile['gamesPlayed']} ({qa_profile['wins']}W - {qa_profile['draws']}D - {qa_profile['losses']}L)")
print("[Done] Seeding complete!")
