import os
import random
import subprocess
import datetime
from notecli import storage
from auto_updater.notify import notify

SAMPLE_NOTES = [
    "Сегодня сделал хороший прогресс в проекте!",
    "Напоминание: проверить задачу на GitHub Actions.",
    "Идея: добавить поддержку тегов в заметках.",
    "Надо подумать о тестах для поиска."
]

def modify_notes():
    action = random.choice(["add", "edit"])

    if action == "add" or not storage.list_notes():
        text = random.choice(SAMPLE_NOTES) + f" ({datetime.datetime.now().isoformat()})"
        filename = storage.save_note(text)
        return f"Added new note {os.path.basename(filename)}"
    else:
        notes = storage.list_notes()
        file = random.choice(notes)
        path = os.path.join(storage.NOTES_DIR, file)
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n[AutoUpdate] " + random.choice(SAMPLE_NOTES))
        return f"Edited note {file}"

def git_commit_and_push(message: str):
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)
    subprocess.run(["git", "push"], check=True)

def main():
    msg = modify_notes()
    try:
        git_commit_and_push(msg)
        notify(f"Committed: {msg}")
    except Exception as e:
        notify(f"Commit failed: {e}")

if __name__ == "__main__":
    main()

