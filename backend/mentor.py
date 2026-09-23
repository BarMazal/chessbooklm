import os
import asyncio
import subprocess
from typing import Dict, Any, Optional
from backend.config import NOTEBOOKLM_NOTEBOOK_ID, NOTEBOOKLM_AUTH_TOKEN

class MentorService:
    """
    Pluggable AI Chess Mentor Service.
    Queries NotebookLM via notebooklm-py, or falls back to smart chess heuristics.
    """

    def __init__(self, notebook_id: str = "", auth_token: str = ""):
        self.notebook_id = notebook_id or NOTEBOOKLM_NOTEBOOK_ID
        self.auth_token = auth_token or NOTEBOOKLM_AUTH_TOKEN

    async def query_mentor(self, prompt: str, notebook_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Sends query to NotebookLM notebook, or uses smart heuristic mentor fallback.
        """
        target_notebook = notebook_id or self.notebook_id

        # 1. Attempt notebooklm-py query if notebook_id is present
        if target_notebook:
            res = await self._query_notebooklm_py(prompt, target_notebook)
            if res.get("success"):
                return {
                    "provider": "NotebookLM (notebooklm-py)",
                    "response": res["text"],
                    "notebook_id": target_notebook
                }

        # 2. Intelligent Heuristic Mentor Fallback
        heuristic_response = self._generate_heuristic_explanation(prompt)
        return {
            "provider": "Chess AI Mentor (Local Strategy Engine)",
            "response": heuristic_response,
            "notebook_id": target_notebook or "None (Set up NotebookLM ID in settings)"
        }

    async def _query_notebooklm_py(self, prompt: str, notebook_id: str) -> Dict[str, Any]:
        """
        Interacts with notebooklm-py package via Python API or CLI executable.
        """
        # Attempt python package import call
        try:
            from notebooklm import NotebookLMClient
            client = NotebookLMClient()
            response_text = await asyncio.to_thread(client.ask, notebook_id=notebook_id, query=prompt)
            if response_text:
                return {"success": True, "text": str(response_text)}
        except ImportError:
            pass
        except Exception as e:
            print(f"[MentorService] notebooklm Python API call failed: {e}")

        # Attempt notebooklm CLI execution as fallback
        try:
            process = await asyncio.create_subprocess_exec(
                "notebooklm", "query", "--notebook-id", notebook_id, prompt,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0 and stdout:
                return {"success": True, "text": stdout.decode("utf-8").strip()}
            else:
                err_msg = stderr.decode("utf-8").strip() if stderr else "Unknown CLI error"
                print(f"[MentorService] notebooklm CLI query returned non-zero code: {err_msg}")
        except Exception as e:
            print(f"[MentorService] notebooklm CLI execution error: {e}")

        return {"success": False, "text": ""}

    def _generate_heuristic_explanation(self, prompt: str) -> str:
        """
        Generates structured, instructive chess advice when NotebookLM is not yet linked.
        """
        # Simple extraction of key details from prompt
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

*(Tip: Connect your Google NotebookLM notebook in settings to get direct book quotes, grandmaster game references, and customized textbook lessons!)*
"""
