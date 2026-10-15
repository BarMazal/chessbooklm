# Changes Log (handover notes for AG)

This file records code, design and requirement changes made outside AG's sessions, so work can be
picked up without guessing. Newest entry first.

---

## 2026-10-15 (part 2): Game lifecycle, undo branches, back-rank motif

**By:** Claude Code. Not committed yet.

### Requirements from the user

1. **No game on app load.** The app must not start a game when it loads, only on **Quick Start / New
   Game**.
2. **Mate recorded twice.** The last (mating) move of a game was recorded a second time in a new
   one-move session. Find and fix the bug.
3. **Undo and branches.** A branch should start only at the first new move after a sequence of undos,
   and only if that move differs from the line that was taken back. Replaying the same move continues
   the same line.
4. **Back rank** is not only mate threats. A back-rank capture combined with a check is also this
   motif.

### Root causes found

- **Double bot move.** Several code paths call `checkAndTriggerAutoMove()`. A second timer could fire
  while `makeBotMove()` was still waiting for `/api/bot-move`, so both replies were played. That
  duplicated moves in the history (e.g. "Nxe4, Nxe4"). For the mating move, the first copy finalized the
  game (`activeLiveGameEvent = null`) and the second copy started a new event containing only the mate.
- **Recorder resumed old games.** When `activeLiveGameEvent` was null, the recorder searched the profile
  for **any** event with `result === 'in_progress'` and appended to it. A new game after a page reload
  therefore continued an old game's event. This, plus the undo-parent bug fixed in part 1, caused the
  broken move chains.
- **Two auto-starts.** Both `DOMContentLoaded` handlers called `startNewGame()` on load.

### Changes (`frontend/app.js`)

- **`isGameActive` flag**, false on load:
  - `showIdleBoard()` shows the start position, paused.
  - While idle, moves can be explored, but nothing is recorded, clocks don't run, and the bot doesn't
    move (`checkAndTriggerAutoMove`, `onMoveExecutedClockTick`, `recordLiveMoveToActiveEvent` all check
    it).
  - `startNewGame()` sets the flag.
  - "Resume" while idle starts a new game if the board is empty; otherwise it tells the user to use
    New Game.
- **Move guards:**
  - `executeMove()` ignores a call while another move is being applied, and ignores moves that are not
    in `legalMoves`.
  - `makeBotMove()` has an in-flight guard (`botMoveInFlight`). Its body moved to
    `requestAndPlayBotMove()`, which drops the engine reply if the position changed while it waited.
- **Recorder event handling:**
  - It always creates a fresh event when `activeLiveGameEvent` is null; it never resumes an old one.
  - `startNewGame()` calls `closeStaleLiveEvents()`, which marks leftover `in_progress` events as
    `result: 'unfinished'`.
  - Nothing is recorded while a history position is being viewed (`liveGameSnapshot` set).
- **Undo / branch model:**
  - Undo only sets `leaf_termination: 'abandoned_undo'` on the last active node; its `branch_id` stays
    `mainline` while the move is "taken back but pending".
  - On the next move from that parent: if the same `move_uci` is played, the taken-back node is
    **revived** (`leaf_termination = null`, time metrics updated) and no new node is created.
  - If a different move is played, the taken-back node and its taken-back descendants are relabelled
    `undo_attempt_N` (N = next free number), and the new move continues `mainline`.
  - The **mainline** is now `branch_id === 'mainline' && leaf_termination !== 'abandoned_undo'`. The
    History tab shows one group per `undo_attempt_N`, plus a "Taken back" group for pending ones.
    `loadProfileEventToBoard` uses the same rule.

### Changes (`backend/move_analysis.py`)

- **`back_rank` covers more cases.** A rook or queen move onto the enemy back rank (enemy king on that
  rank) counts when it is:
  - mate: 95 (100 when the move itself mates);
  - a check that captures: 55 + 4 × captured value;
  - a check on a king that can't leave its back rank: 45.

  It counts both as a threat (`detect_opportunities`) and as a move-intrinsic `motifs_for` entry. The
  label is now "Back-Rank Threat".
- **New test:** `test_back_rank_check_that_wins_material`. 26 tests pass.

### Data touched during testing

- `prof_default` → "Live Match (11:22 PM)" was left `in_progress` by an old page load. It is now
  `unfinished` (by the new rule). Its 6 moves are unchanged (they match git HEAD).
- Test games created during verification were deleted.

---

## 2026-10-15: History node analysis rebuilt on real data (schema v2)

**By:** Claude Code (AG was out of quota). Nothing is committed yet; all changes are in the working tree
on `master`, on top of AG's own uncommitted work from commit `e9004d8`.

### Why

Review of the node JSON (move `1.e4`, QA profile) showed most of the "analysis" was not real:

- **⚡ SF Move never ran Stockfish.** `computeAnalysisPayloadForNode` invented evals from the node's index
  (`(index % 7 - 3) * 0.12`).
- **Mentor failures were hidden.** When NotebookLM failed, `generate_heuristic_node_analysis` filled in
  fixed template sentences under the label `source: "Chess AI Mentor (Local Strategy Engine)"`.
- **Pattern detectors fired in almost every position.** For example, `back_rank_weakness` was true in
  every opening, and `discovered_threats` was true whenever any slider attacked anything.
  `primary_motif` was simply the first true flag in the list.
- **The move sequence included future moves and duplicates.** At White's move 1 it was
  `e4 -> e4 -> e4 -> e6`, so the opening was named "French Defense" after 1.e4 alone.
- **Every analysis block was stored 4–5 times per node:** top level, `per_move_analysis`, two copies in
  `per_sequence_analysis`, and `mentor_*`.
- **Other fake paths:**
  - `triggerSelectiveDagAnalysis` (Advanced Analytics → "Analyze") showed a progress animation and
    marked every node `ANALYZED`.
  - `handleLiveMoveUndo` hard-coded every undone move as a Blunder with eval delta -1.85.
  - Saved games wrote placeholder `per_move_analysis` (`'+0.0'`, `'Good'`) and marked themselves
    `ANALYZED`.
- **The bundled Stockfish never started on Windows.** The relative path `stockfish/stockfish.exe` failed
  with WinError 2. The app then fell back to Lichess cloud, which had a bug (`board` undefined), and then
  to a material count. So live evals were not Stockfish either.

### Requirements agreed with the user (Guy)

1. **Per-move commands for every profile, not only QA.** Right-clicking a move chip in History opens
   **📈 Stockfish Analysis / 🧠 Mentor Analysis / 🔍 Show Analysis**.
2. **Mentor depends on Stockfish.** Mentor analysis needs engine facts. If Stockfish has not analysed the
   node yet, the mentor action runs it first (move + sequence window).
3. **No mentor output without NotebookLM.** If NotebookLM is not connected or does not return JSON,
   `mentor` stays **null** and the user sees the reason. Mentor text is never generated locally. Some
   hallucination from NotebookLM is acceptable.
4. **Motif rules:**
   - **Back rank:** counts only if *this move* creates a back-rank mate threat (or allows one against
     the mover).
   - **Discovered attack:** counts only for a slider that did *not* move. The moved piece opened the
     line.
   - **Scores:** every motif has a 0–100 score. The **primary motif is the highest score**.
   - **No pattern:** if nothing is detected, the move is `book` or `quiet`. No pattern is forced.
5. **Six aspects** are **0–100 scores**, not true/false.
6. **Motifs are split into for and against:**
   - `motifs_for`: what this move created.
   - `motifs_against`: opponent chances that this move *allowed* or *ignored*.

   This split is what makes repeated-error tracking possible.
7. **Wipe old analysis.** All old analysis on the existing nodes was wiped (not converted) and will be
   re-run.
8. **Order of work:** real Stockfish first, then everything that depends on it.

### New node schema (one copy of everything)

Raw recording fields are unchanged: `id, event_id, profile_id, move_number, color, move_san, move_uci,
fen (after), parent_id, branch_id, leaf_termination, time_control_metrics`. All analysis now lives in
**one** field:

```jsonc
"analysis": null | {
  "schema_version": 2,
  "context": { "phase", "opening": {"eco","name","is_book_move"}, "move_number", "color", "move_san",
               "fen_before", "fen_after" },
  "engine":  { "eval_before","eval_after" /* White POV pawns, null if mate */, "mate_before","mate_after",
               "eval_delta" /* mover POV */, "cp_loss", "win_prob_before","win_prob_after" /* mover, 0-100 */,
               "best_move_uci","best_move_san","played_is_best",
               "quality" /* Book|Best|Good|Inaccuracy|Mistake|Blunder */, "missed_opportunity","missed_mate",
               "depth","source","analyzed_at" },
  "move":    { "aspects": { "building_state","seizing_opportunity","score",
                            "preventing_opponent_building_state","avoiding_opponent_seizing_opportunity",
                            "opponent_score" },            // 0-100 each
               "motifs_for":     [{ "id","score","status":"created","detail" }],
               "motifs_against": [{ "id","score","status":"allowed|ignored","detail" }],
               "primary_motif":  { "id","side":"for|against","score" } | null,
               "category": "book|tactical|positional|quiet", "is_check", "is_capture" },
  "sequence": { "window_plies" /* 6 */, "moves", "eval_change","eval_trend", "aspects" /* avg of mover's plies */,
                "errors": {"Inaccuracy","Mistake","Blunder"}, "motifs_for","motifs_against", "analyzed_at" },
  "mentor":   { "move_comment","sequence_comment","key_idea","drill" /* only for Inaccuracy/Mistake/Blunder */,
                "source","analyzed_at" }      // ONLY from NotebookLM
}
```

- **Removed** (deleted by migration): `per_move_analysis, per_sequence_analysis, mentor_move_analysis,
  mentor_sequence_analysis, six_aspect_metrics, six_aspect_flags, general_classification, context,
  stockfish_analysis_status, mentor_analysis_status, analysis_status, running_error_metrics`.
- **Added:** `analysis_error` (string) is set on a node whose move chain cannot be rebuilt.
- **Live recordings** now store `analysis: null`. Running error counts are worked out from the analysed
  ancestors when the mentor is called (`game_errors`), not stored.

**Motif ids:**
`fork, pin, skewer, discovered_attack, hanging_piece, back_rank, mate_threat, overloaded_defender,
trapped_piece` (tactical) and `battery, passed_pawn, outpost, open_file, seventh_rank, exposed_king,
pawn_weakness, simplification` (positional). Labels and descriptions are in `MOTIF_INFO`
(`backend/move_analysis.py`). The frontend loads them from `GET /api/analysis/motifs`.

The old ids (`forks`, `pins`, `back_rank_weakness`, `flanks`, `interference`, `diagonal_pin`, …) are
gone.

### How the scoring works (`backend/move_analysis.py`)

- **New vs. existing patterns.** `detect_opportunities(board, side)` returns keyed patterns.
  - `motifs_for` = the mover's patterns after the move whose key did not exist before. This is how
    "this move created it" is enforced.
  - `motifs_against` = the opponent's patterns after the move. They are `allowed` if new. They are
    `ignored` if they already existed and the motif is a real threat (hanging piece, fork, mate, back
    rank, trapped piece, skewer); ignored threats count at 0.8 of their score.
- **Engine check on patterns:**
  - If cp_loss < 50, tactical `motifs_against` are scaled ×0.4: the threat was not real.
  - If cp_loss ≥ 150, they are scaled ×1.25: the threat is confirmed.
  - If cp_loss > 150, every `motifs_for` entry is scaled ×0.5: what the move built did not hold up.
- **Quality:**
  - **Best:** the played move is the engine's best, or cp_loss ≤ 10.
  - **Book:** the move is inside a known ECO line and cp_loss ≤ 50.
  - Otherwise by the drop in winning chances (Lichess model): **Inaccuracy** ≥ 5, **Mistake** ≥ 10,
    **Blunder** ≥ 15 percentage points.
  - **Missing a forced mate** is at least an Inaccuracy (a Mistake if the eval falls below +5).
- **Aspects** are documented in the module docstring. In short:
  - **building_state:** positional patterns created + mobility gained + development/castling in the
    opening.
  - **seizing_opportunity:** the strongest tactical pattern created.
  - **score:** material won by this move.
  - **preventing_opponent_building_state:** opponent mobility cut + opponent patterns removed.
  - **avoiding_opponent_seizing_opportunity:** 100 minus the worse of (the strongest opponent tactic,
    cp_loss/3).
  - **opponent_score:** drop in winning chances ×2.

### API changes (`backend/main.py`)

| Endpoint | Status |
|---|---|
| `GET /api/analysis/motifs` | **new**: motif catalog |
| `POST /api/analysis/move` | **new**: `{start_fen, uci_path[], move_number, expected_fen_after?, depth?}` → `{success, analysis}`. Replays the path from `start_fen`, so missing intermediate FENs (saved games) are fine. Returns `success:false` if no real engine is available. |
| `POST /api/analysis/sequence` | **new**: `{color, plies[]}` (oldest first, each with context/engine/move) → `{sequence}` |
| `POST /api/analysis/repair-chain` | **new**: rebuilds `parent_id` links by matching positions (parent FEN + move = child FEN). Used automatically when a chain is broken. |
| `POST /api/mentor/node-analysis` | **rewritten**: `{node_id, analysis, time_control_metrics, game_errors, analysis_type}`. Requires `analysis.engine` (400 otherwise). Returns `{success, mentor}`, or `{success:false, mentor:null, error}`. |
| `POST /api/mentor/batch-node-analysis` | **removed** (unused) |
| `GET /api/analytics/profile-insights` | reads the v2 schema |

Supporting changes:

- **`MentorService.query_mentor`** now returns `connected: true/false`. This is the only signal used to
  accept mentor output.
- **`ChessEngineManager`:**
  - Engine paths resolve against the project root, which fixes the Windows launch failure.
  - New `analyse_for_review()` returns real evals only (local Stockfish, else Lichess cloud, else
    `None`; never the material count) and caches by FEN+depth.
  - The cloud-eval `board` bug is fixed.
  - The engine is closed at interpreter exit, so tests no longer hang.
- **`ChessTranslator.classify_move_and_position`** was removed (superseded by `move_analysis.py`).

### Frontend changes (`frontend/app.js`)

- **Removed fake generators:** `computeAnalysisPayloadForNode`, `computeNodeContextAndClassifications`,
  `applyStructuredAnalysisToNode`, `getMentor*` template helpers, and a duplicate
  `cancelActiveHistoryAnalysis`.
- **New runners** (section "Node analysis (schema v2)"):
  - `getNodeAncestry` follows the `parent_id` chain. It no longer filters by move number, which is what
    let future moves into the sequence.
  - `runEngineAnalysisForNode`, `runSequenceAnalysisForNode` and `runMentorAnalysisForNode` (the mentor
    one auto-runs SF first).
  - `repairEventChain` and `runAtomicAnalysisBatch`. The batch stops at once if the engine or NotebookLM
    is unavailable; otherwise it saves per node as before.
- **Right-click on move chips** (History tab and QA explorer) uses `openMoveContextMenu`. The result is
  shown by `openNodeAnalysisPopup`, which works for every profile. The QA pane's 🧠 Mentor Analyze button
  uses the same path.
- **Consumers moved to v2:** badges and missing counts, chip colours, `buildProfileDagTree` (repeated
  errors are keyed by the top `motifs_against` id on Mistake/Blunder nodes), the QA explorer and the DAG
  node browser.
- **"Analyze pending nodes"** in Advanced Analytics now runs the real SF Move + SF Seq batches.
- **Live recorder:**
  - It no longer classifies moves; only the stress index uses the live eval swing.
  - The parent is now the last move **not taken back**: `lastActiveLiveNode()`.
  - Undo marks that node `abandoned_undo` without faking a Blunder.
- **Migration:** `migrateProfileNodesToAnalysisV2()` runs after loading from localStorage and after
  merging backend profiles. It strips the legacy keys and nulls any non-v2 `analysis`. The old QA rule
  that wiped QA analysis on every load was removed; analysis now persists.

### Data

- `backend/user_profiles.json`: legacy analysis was removed from all 880 nodes (`analysis: null`).
  During testing, real v2 analysis was written for about 190 QA nodes.
- Recordings made by the old buggy recorder are repaired automatically on first analysis. One QA event
  ("Live Match (10:43 PM)", a single node at move 48 with no earlier position) cannot be rebuilt and
  keeps `analysis_error`.

### Tests

- `backend/test_structured_analysis.py` was rewritten. It covers:
  - book 1.e4 with no forced patterns, and the opening named only from moves played;
  - the fork, discovered check and hanging-piece blunder cases;
  - back rank counted only when allowed, and a missed mate not graded Good;
  - no engine → null engine fields, and sequence aggregation;
  - the endpoints: path replay, broken chain, FEN mismatch, and mentor requiring the engine.
- Run with `venv\Scripts\python.exe -m unittest backend.test_structured_analysis backend.test_app`
  (25 tests, all passing). pytest is not installed in the venv.

### Open points / ideas for next steps

- **Mentor run with NotebookLM connected:** never tested here (NotebookLM was not connected in the test
  server). The prompt asks for `{move_comment, sequence_comment, key_idea, drill}`.
- **Mentor batch** uses one NotebookLM call per node (≈ 870 calls for QA). Consider limiting it to
  Inaccuracy/Mistake/Blunder nodes.
- **Detector heuristics** (hanging/pin/fork) still ignore some defensive resources (pinned attackers, …).
  The engine check limits the damage, but they are heuristics.
- **Live recorder move number/colour** is still derived from `moveHistory` length. That is wrong for
  games started from a custom FEN with Black to move.
- **Old single-node event:** QA "Live Match (10:43 PM)" (one node, `Qee8#`) is a leftover of the
  double-bot-move bug fixed in part 2 above. It can be deleted.
- **Old placeholder code** (`_generate_heuristic_explanation` in `mentor.py`) still feeds *other*
  features (live coaching, quiz, etc.). They were not touched in this change.
- **Restart required:** restart the running server (`run.ps1`) so the new endpoints and the Stockfish
  path fix take effect. The old process keeps old data in memory and could write it back to
  `user_profiles.json` on sync.
