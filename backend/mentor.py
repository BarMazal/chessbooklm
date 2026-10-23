import os
import json
import asyncio
import subprocess
import tempfile
from typing import Dict, Any, List, Optional
from backend.config import NOTEBOOKLM_NOTEBOOK_ID, NOTEBOOKLM_AUTH_TOKEN

# Dedicated isolated profile name for this project to prevent interference with other local apps
PROJECT_PROFILE_NAME = "chessbooklm"

class MentorService:
    """
    Pluggable AI Chess Mentor Service.
    Queries NotebookLM via notebooklm-py using a project-isolated profile ('chessbooklm')
    to prevent interference with any other application on your machine.
    """

    def __init__(self, notebook_id: str = "", auth_token: str = ""):
        self.notebook_id = notebook_id or NOTEBOOKLM_NOTEBOOK_ID
        self.auth_token = auth_token or NOTEBOOKLM_AUTH_TOKEN
        self.active_profile = PROJECT_PROFILE_NAME

    def _get_notebooklm_cmd(self) -> str:
        venv_cmd = os.path.join(os.getcwd(), "venv", "Scripts", "notebooklm.exe")
        if os.path.exists(venv_cmd):
            return venv_cmd
        venv_cmd_posix = os.path.join(os.getcwd(), "venv", "bin", "notebooklm")
        if os.path.exists(venv_cmd_posix):
            return venv_cmd_posix
        return "notebooklm"

    def _build_cmd(self, *args) -> List[str]:
        """
        Injects --profile chessbooklm into every command to isolate credentials & storage.
        """
        cmd = [self._get_notebooklm_cmd(), "--profile", self.active_profile]
        cmd.extend(args)
        return cmd

    async def get_auth_status(self) -> Dict[str, Any]:
        """
        Checks authentication status using `notebooklm --profile chessbooklm doctor --json`.
        """
        try:
            cmd = self._build_cmd("doctor", "--json")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            if stdout:
                data = json.loads(stdout.decode("utf-8", errors="ignore"))
                auth_pass = data.get("checks", {}).get("auth", {}).get("status") == "pass"
                auth_detail = data.get("checks", {}).get("auth", {}).get("detail", "")
                return {
                    "is_logged_in": auth_pass,
                    "profile": data.get("profile", self.active_profile),
                    "detail": auth_detail,
                    "active_notebook_id": self.notebook_id
                }
        except Exception as e:
            print(f"[MentorService] Auth status check failed: {e}")

        return {
            "is_logged_in": False,
            "profile": self.active_profile,
            "detail": "Not authenticated",
            "active_notebook_id": self.notebook_id
        }

    async def trigger_login(self, email: Optional[str] = None, fresh: bool = True, profile_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Spawns notebooklm login command in background using isolated project profile.
        Setting fresh=True forces a clean session so Google prompts for User Email & Password.
        """
        try:
            target_profile = profile_name or self.active_profile
            cmd = [self._get_notebooklm_cmd(), "--profile", target_profile, "login"]

            # Force fresh session to prompt for email/password instead of reusing default profile
            if fresh:
                cmd.append("--fresh")

            print(f"[MentorService] Executing login command: {' '.join(cmd)}")
            subprocess.Popen(cmd)
            return {
                "success": True,
                "message": f"Fresh login browser window launched for isolated profile '{target_profile}'. Please enter your Google Email & Password in the browser window.",
                "profile": target_profile
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to launch fresh browser login: {str(e)}"
            }

    async def list_profiles(self) -> List[Dict[str, Any]]:
        """
        Lists all available notebooklm account profiles.
        """
        try:
            cmd = [self._get_notebooklm_cmd(), "profile", "list"]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            if stdout:
                lines = stdout.decode("utf-8", errors="ignore").splitlines()
                profiles = []
                for l in lines:
                    line_clean = l.strip()
                    if line_clean and not line_clean.startswith("─") and not line_clean.startswith("┌") and "Profile" not in line_clean:
                        parts = [p.strip() for p in line_clean.split("│") if p.strip()]
                        if parts:
                            p_name = parts[0].replace("*", "").strip()
                            profiles.append({"name": p_name, "is_active": p_name == self.active_profile})
                if not profiles:
                    profiles = [{"name": self.active_profile, "is_active": True}]
                return profiles
        except Exception as e:
            print(f"[MentorService] Profile list error: {e}")

        return [{"name": self.active_profile, "is_active": True}]

    async def switch_profile(self, profile_name: str) -> Dict[str, Any]:
        """
        Switches active notebooklm profile.
        """
        self.active_profile = profile_name
        return {
            "success": True,
            "message": f"Switched to profile '{profile_name}'.",
            "profile": profile_name
        }

    async def logout(self) -> Dict[str, Any]:
        """
        Logs out of the current project profile by clearing stored credentials.
        """
        try:
            cmd = self._build_cmd("auth", "logout")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            await process.communicate()
            return {
                "success": True,
                "message": f"Logged out profile '{self.active_profile}'. Saved credentials cleared."
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Logout failed: {str(e)}"
            }

    async def import_cookies(self, cookies_json_str: str) -> Dict[str, Any]:
        """
        Imports authentication cookies from JSON content for the isolated profile.
        """
        try:
            cookies_data = json.loads(cookies_json_str)
            
            with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8") as tf:
                json.dump(cookies_data, tf)
                temp_path = tf.name

            cmd = self._build_cmd("auth", "import-cookies", temp_path)
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            try:
                os.remove(temp_path)
            except Exception:
                pass

            if process.returncode == 0:
                return {"success": True, "message": f"Cookies imported into profile '{self.active_profile}' successfully!"}
            else:
                err = stderr.decode("utf-8", errors="ignore") if stderr else "Import failed"
                return {"success": False, "message": f"Cookie import failed: {err}"}
        except json.JSONDecodeError:
            return {"success": False, "message": "Invalid JSON format. Please provide valid Google cookie JSON."}
        except Exception as e:
            return {"success": False, "message": f"Import error: {str(e)}"}

    async def list_notebooks(self) -> List[Dict[str, Any]]:
        """
        Lists all available NotebookLM notebooks for the project profile.
        """
        try:
            cmd = self._build_cmd("list", "--json")
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            try:
                # `notebooklm list` typically takes 4-5s; a 3s limit made auto-selection always fail
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=15.0)
            except asyncio.TimeoutError:
                try:
                    process.kill()
                except Exception:
                    pass
                return []
            if process.returncode == 0 and stdout:
                raw_text = stdout.decode("utf-8", errors="ignore").strip()
                data = json.loads(raw_text)
                notebooks_raw = data.get("notebooks", [])
                result = []
                for nb in notebooks_raw:
                    nb_id = nb.get("id")
                    result.append({
                        "id": nb_id,
                        "title": nb.get("title") or f"Notebook {nb_id[:8] if nb_id else ''}",
                        "created_at": nb.get("created_at"),
                        "is_active": nb_id == self.notebook_id
                    })
                return result
            else:
                err = stderr.decode("utf-8", errors="ignore") if stderr else "Unknown error"
                print(f"[MentorService] notebooklm list returned non-zero code: {err}")
        except Exception as e:
            print(f"[MentorService] Failed to list notebooks: {e}")
        return []

    async def query_mentor(self, prompt: str, notebook_id: Optional[str] = None, timeout: float = 60.0) -> Dict[str, Any]:
        """
        Sends query to NotebookLM notebook, or falls back to smart strategy engine.
        `timeout` bounds the NotebookLM `ask` call; long structured prompts can take ~1 minute.
        The result carries `connected` and, when not connected, `error_reason`
        ("no_notebook" | "timeout" | "cli_error").
        """
        target_notebook = notebook_id or self.notebook_id

        # Auto-select notebook if not set
        if not target_notebook:
            notebooks = await self.list_notebooks()
            if notebooks:
                chess_nb = next((n for n in notebooks if "chess" in n.get("title", "").lower()), None)
                if chess_nb:
                    target_notebook = chess_nb["id"]
                else:
                    target_notebook = notebooks[0]["id"]
                self.notebook_id = target_notebook

        error_reason = "no_notebook"
        if target_notebook:
            res = await self._query_notebooklm_py(prompt, target_notebook, timeout=timeout)
            error_reason = res.get("error_reason", "cli_error")
            if res.get("success"):
                return {
                    "provider": f"NotebookLM ({target_notebook[:8]}...)",
                    "response": res["text"],
                    "notebook_id": target_notebook,
                    "connected": True
                }

        heuristic_response = self._generate_heuristic_explanation(prompt)
        return {
            "provider": "Chess AI Mentor (Local Strategy Engine)",
            "response": heuristic_response,
            "notebook_id": target_notebook or "None (Select a NotebookLM notebook)",
            "connected": False,
            "error_reason": error_reason
        }

    async def _query_notebooklm_py(self, prompt: str, notebook_id: str, timeout: float = 60.0) -> Dict[str, Any]:
        """
        Queries NotebookLM notebook via CLI ask subcommand with --json to retrieve grounded AI answer.
        """
        try:
            cmd = self._build_cmd("ask", "-n", notebook_id, "--json", prompt)
            try:
                print(f"[MentorService] Running ask command: {prompt[:60]}...")
            except Exception:
                pass
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                try:
                    process.kill()
                except Exception:
                    pass
                print(f"[MentorService] notebooklm ask timed out after {timeout:.0f}s; falling back to local engine.")
                return {"success": False, "text": "", "error_reason": "timeout"}

            if process.returncode == 0 and stdout:
                raw_out = stdout.decode("utf-8", errors="ignore").strip()
                try:
                    data = json.loads(raw_out)
                    if isinstance(data, dict) and "answer" in data:
                        answer_text = data["answer"]
                        # Format references if present
                        refs = data.get("references", [])
                        if refs:
                            citations = []
                            for r in refs:
                                c_num = r.get("citation_number")
                                c_text = r.get("cited_text", "").strip()
                                if c_num and c_text:
                                    citations.append(f"> **[{c_num}]** {c_text}")
                            if citations:
                                answer_text += "\n\n### 📖 Book Sources & Citations:\n" + "\n\n".join(citations)
                        return {"success": True, "text": answer_text}
                    elif isinstance(data, str):
                        return {"success": True, "text": data}
                except Exception as parse_err:
                    print(f"[MentorService] Failed to parse JSON response: {parse_err}")
                    return {"success": True, "text": raw_out}
            else:
                err_msg = stderr.decode("utf-8", errors="ignore").strip() if stderr else "Unknown error"
                print(f"[MentorService] notebooklm ask failed (code {process.returncode}): {err_msg}")
        except Exception as e:
            print(f"[MentorService] notebooklm ask exception: {e}")

        return {"success": False, "text": ""}

    def _generate_heuristic_explanation(self, prompt: str) -> str:
        lines = prompt.split("\n")
        eval_line = next((l for l in lines if "Evaluation:" in l or "Score:" in l), "Equally balanced position.")
        opening_line = next((l for l in lines if "Identified Opening:" in l or "Opening:" in l), "Standard Opening Position.")
        move_line = next((l for l in lines if "Top Recommended Move by Engine:" in l or "Top Recommended Move" in l or "suggests" in l), "Develop key pieces.")
        reviewed_line = next((l for l in lines if "CURRENT REVIEWED MOVE:" in l), None)

        # Extract concrete tactical comparison
        tactical_comp = []
        if "- CONCRETE TACTICAL COMPARISON:" in prompt:
            t_part = prompt.split("- CONCRETE TACTICAL COMPARISON:")[1].split("- USER INQUIRED ALTERNATIVE CANDIDATE MOVES:")[0].split("- King & Tactical Status:")[0].strip()
            tactical_comp = [l.strip() for l in t_part.split("\n") if l.strip().startswith("*")]

        # Extract user inquired candidate moves
        candidate_lines = []
        if "- USER INQUIRED ALTERNATIVE CANDIDATE MOVES:" in prompt:
            cand_part = prompt.split("- USER INQUIRED ALTERNATIVE CANDIDATE MOVES:")[1].split("- King & Tactical Status:")[0].strip()
            candidate_lines = [l.strip() for l in cand_part.split("\n") if l.strip().startswith("* Move")]

        # Extract user custom question
        user_query = None
        if "USER QUERY / DISCUSSION ITEM:" in prompt:
            uq_part = prompt.split("USER QUERY / DISCUSSION ITEM:")[1].split("SPECIAL FORMATTING INSTRUCTIONS:")[0].strip()
            if uq_part and not uq_part.startswith("Explain why Stockfish recommends"):
                user_query = uq_part

        is_follow_up = "PRIOR CONVERSATION HISTORY" in prompt

        if reviewed_line and (user_query or is_follow_up):
            rev_clean = reviewed_line.replace("- CURRENT REVIEWED MOVE:", "").strip()
            m_played = rev_clean.split(" was played")[0].strip() if " was played" in rev_clean else "the played move"
            m_best = rev_clean.split("Recommended best move was ")[1].split(".")[0].strip() if "Recommended best move was " in rev_clean else "the recommended move"
            m_qual = rev_clean.split("evaluated as a ")[1].split()[0].strip() if "evaluated as a " in rev_clean else "Move"

            played_points = [tc.replace("* What went wrong with ", "").replace("* ", "") for tc in tactical_comp if "What went wrong" in tc]
            best_points = [tc.replace("* Why ", "").replace("* ", "") for tc in tactical_comp if "Why " in tc or "decisive" in tc]

            played_desc = "\n".join([f"* **{p}**" for p in played_points]) if played_points else f"* **Conceding Initiative & Tempo:** Moving **{m_played}** was too passive for this active position. Instead of maintaining pressure or invading the opponent's ranks, it conceded crucial tempi and allowed the opponent time to consolidate."
            best_desc = "\n".join([f"* **{p}**" for p in best_points]) if best_points else f"* **Forcing Infiltration & Activity:** In contrast, **{m_best}** immediately seizes the initiative by creating concrete forcing threats (infiltrating key ranks, attacking loose pieces, or winning tempo), giving the opponent no time to untangle."

            cand_block = ""
            if candidate_lines:
                cand_bullets = "\n".join([f"* **{cl.replace('* Move ', 'Candidate ')}**" for cl in candidate_lines])
                cand_block = f"""

#### 🎯 Alternative Moves You Inquired About:
{cand_bullets}
* **Human Practicality vs. Engine Lines:** While engines calculate razor-sharp queen infiltrations, choosing a solid alternative that fits your comfort zone is often superior practical chess. If a candidate move keeps your king safe and avoids tactical blunders, it is a sound human choice."""

            intro_sentence = f"Building upon our previous turns, here is the concrete tactical breakdown between **{m_played}** and **{m_best}**:" if is_follow_up else f"Here is the tactical and strategic breakdown of why **{m_played}** failed and why **{m_best}** was the winning move:"

            return f"""### ♟️ Move Refutation & Tactical Breakdown

{intro_sentence}

#### ❌ What Went Wrong with {m_played} ({m_qual.title()})
{played_desc}
* **The Strategic Concession:** A move is graded as a blunder not just when it drops a piece on the spot, but when it completely surrenders dynamic momentum. Playing **{m_played}** relinquished active pressure, letting the opponent untangle their defenses.

#### ⚡ Why {m_best} Was Decisive
{best_desc}
* **Tempo & Positional Dominance:** **{m_best}** forces the opponent to respond to immediate, multiple threats instead of executing their own plan. It coordinates your forces on dominant ranks/files and maintains maximum pressure.{cand_block}

#### 💡 The Practical Takeaway
When you have the chance to launch an active piece infiltration into the opponent's territory (like **{m_best}**), playing a cautious or passive move like **{m_played}** lets your entire advantage slip away. In critical positions, always prioritize your most forcing candidate moves (checks, captures, and deep penetrations)!
"""

        if reviewed_line:
            rev_clean = reviewed_line.replace("- CURRENT REVIEWED MOVE:", "").strip()
            opening_title = opening_line.replace('- Identified Opening:', '').strip()

            tactical_breakdown_block = ""
            if tactical_comp:
                tactical_items = "\n".join([f"* **{tc.replace('* ', '')}**" for tc in tactical_comp])
                tactical_breakdown_block = f"""
**2. Tactical Cause & Refutation**
{tactical_items}
"""

            candidates_section = ""
            if candidate_lines:
                cand_bullets = "\n".join([f"* **{cl.replace('* Move ', 'Candidate ')}**" for cl in candidate_lines])
                candidates_section = f"""
**4. Evaluated Candidate Alternatives**
{cand_bullets}
* **Human Practicality vs. Engine Lines:** While engines rank moves by fractions of a pawn, choosing a solid alternative that fits your strategic comfort zone is often superior practical chess.
"""

            return f"""### ♟️ Move & Tactical Analysis

**1. Move Review & Evaluation**
* **Played Move Analysis:** {rev_clean}
* **Position Control:** {eval_line.replace('- Stockfish Engine Evaluation:', '').strip()}
{tactical_breakdown_block}
**3. Tactical & Engine Guidance**
* **Next Engine Recommendation:** {move_line.replace('- Top Recommended Move by Engine:', '').strip()}
* **Tactical Tip:** Calculate all opponent forcing replies (checks, captures, and threats) before committing to a move. Ensure you do not leave pieces undefended or skewered.
{candidates_section}
**5. General Strategic Plan ({opening_title})**
* **Pawn Structure:** Maintain central presence or establish pawn chains that support piece outposts.
* **Piece Coordination:** Avoid leaving pieces undefended (LPDO - Loose Pieces Drop Off). Bring rooks to open files and safeguard king mobility.

*(Tip: Log in with your target Google account in the top panel to load your chess books notebook!)*
"""

        return f"""### ♟️ Strategic & Positional Analysis

**1. Position Evaluation & Control**
{eval_line}
In this game phase, key focus areas include controlling the central squares (d4, d5, e4, e5), securing piece coordination, and ensuring King safety before launching pawn pushes or flank attacks.

**2. Tactical & Engine Suggestion**
{move_line}
*   **Why this makes sense:** Moving this piece improves square activity, opens lines of vision for your minor pieces, or relieves direct pressure on undefended targets.
*   **Alternative Ideas:** Always check your opponent's forcing responses (checks, captures, and threats) before committing.

**3. General Strategic Plan ({opening_line.replace('- Identified Opening:', '').strip()})**
*   **Pawn Structure:** Maintain central presence or establish pawn chains that support piece outposts.
*   **Piece Coordination:** Bring Rooks to open or semi-open files, castle early, and avoid leaving pieces un-defended (LPDO - Loose Pieces Drop Off).

*(Tip: Log in with your target Google account in the top panel to load your chess books notebook!)*
"""
