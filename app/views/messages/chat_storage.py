import json
from pathlib import Path

CHAT_FILE = Path("chat_history.json")

def load_chat():
    if CHAT_FILE.exists():
        try:
            with open(CHAT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
    return []

def save_chat(chat):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chat, f, indent=4, ensure_ascii=False)