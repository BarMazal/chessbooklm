import os
from dotenv import load_dotenv

load_dotenv()

STOCKFISH_PATH = os.getenv("STOCKFISH_PATH", "").strip()
NOTEBOOKLM_NOTEBOOK_ID = os.getenv("NOTEBOOKLM_NOTEBOOK_ID", "373f42b4-4dbf-47a5-abec-df72c3a3ffbf").strip() or "373f42b4-4dbf-47a5-abec-df72c3a3ffbf"
NOTEBOOKLM_AUTH_TOKEN = os.getenv("NOTEBOOKLM_AUTH_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
