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

# --- snippet: unique_words_sorted ---
def unique_words_sorted(text: str) -> list:
    """
    Returns sorted list of unique words.
    """
    s = set(w.strip('.,!?()[]') for w in text.split())
    return sorted(w for w in s if w)
# --- endsnippet ---


# autosave 2025-10-02T09:06:02.257175

# autosave 2025-10-02T09:08:01.613227

# --- snippet: levenshtein_distance ---
def levenshtein(a: str, b: str) -> int:
    """
    Compute Levenshtein distance between two strings (iterative DP).
    """
    if a == b:
        return 0
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            add = prev[j] + 1
            delete = cur[j-1] + 1
            change = prev[j-1] + (0 if ca == cb else 1)
            cur[j] = min(add, delete, change)
        prev = cur
    return prev[-1]
# --- endsnippet ---

# AUTO_SNIPPETS_ZONE_END
