import os
from notecli.storage import NOTES_DIR

def search_notes(keyword: str):
    results = []
    for file in os.listdir(NOTES_DIR):
        with open(os.path.join(NOTES_DIR, file), "r", encoding="utf-8") as f:
            content = f.read()
            if keyword.lower() in content.lower():
                results.append((file, content[:80]))
    return results
