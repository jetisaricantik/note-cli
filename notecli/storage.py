import os
import datetime

NOTES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notes")

def ensure_notes_dir():
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)

def save_note(content: str):
    ensure_notes_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(NOTES_DIR, f"note_{timestamp}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def list_notes():
    ensure_notes_dir()
    return sorted(os.listdir(NOTES_DIR))

def read_note(filename: str):
    path = os.path.join(NOTES_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# AUTO_SNIPPETS_ZONE_START
# Здесь авто-апдейтер может вставлять функции из snippets.

# --- snippet: reverse_text ---
def reverse_text(s: str) -> str:
    """
    Reverses text.
    """
    return s[::-1]
# --- endsnippet ---

# AUTO_SNIPPETS_ZONE_END
