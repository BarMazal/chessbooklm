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
            stdout, stderr = await process.communicate()
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

    async def query_mentor(self, prompt: str, notebook_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Sends query to NotebookLM notebook, or falls back to smart strategy engine.
        """
        target_notebook = notebook_id or self.notebook_id

        if target_notebook:
            res = await self._query_notebooklm_py(prompt, target_notebook)
            if res.get("success"):
                return {
                    "provider": f"NotebookLM ({target_notebook[:8]}...)",
                    "response": res["text"],
                    "notebook_id": target_notebook
                }

        heuristic_response = self._generate_heuristic_explanation(prompt)
        return {
            "provider": "Chess AI Mentor (Local Strategy Engine)",
            "response": heuristic_response,
            "notebook_id": target_notebook or "None (Select a NotebookLM notebook)"
        }

    async def _query_notebooklm_py(self, prompt: str, notebook_id: str) -> Dict[str, Any]:
        """
        Queries NotebookLM notebook via CLI ask subcommand.
        """
        try:
            cmd = self._build_cmd("ask", "--notebook-id", notebook_id, prompt)
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0 and stdout:
                output_text = stdout.decode("utf-8", errors="ignore").strip()
                return {"success": True, "text": output_text}
            else:
                err_msg = stderr.decode("utf-8", errors="ignore").strip() if stderr else "Unknown error"
                print(f"[MentorService] notebooklm ask failed: {err_msg}")
        except Exception as e:
            print(f"[MentorService] notebooklm ask exception: {e}")

        return {"success": False, "text": ""}

    def _generate_heuristic_explanation(self, prompt: str) -> str:
        lines = prompt.split("\n")
        eval_line = next((l for l in lines if "Evaluation:" in l or "Score:" in l), "Equally balanced position.")
        opening_line = next((l for l in lines if "Opening:" in l), "Standard Opening Position.")
        move_line = next((l for l in lines if "Top Recommended Move" in l or "suggests" in l), "Develop key pieces.")

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
