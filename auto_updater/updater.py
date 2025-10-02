import os
import sys
import random
import re
import subprocess
from datetime import datetime

# Добавляем корень проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from auto_updater.notify import notify

# Пути
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SNIPPETS_DIR = os.path.join(ROOT, "data", "snippets_code")
TARGET_DIRS = [os.path.join(ROOT, "notecli")]

# Настройки вероятностей
PROB_ADD = 0.6      # вероятность добавить сниппет
PROB_DELETE = 0.2   # вероятность удалить сниппет

SNIPPET_HEADER = re.compile(r"# --- snippet: (.+?) ---")
SNIPPET_END = re.compile(r"# --- endsnippet ---")

def load_all_snippets():
    snippets = {}
    for fname in os.listdir(SNIPPETS_DIR):
        path = os.path.join(SNIPPETS_DIR, fname)
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        starts = list(SNIPPET_HEADER.finditer(text))
        for s in starts:
            name = s.group(1).strip()
            start_idx = s.end()
            m_end = SNIPPET_END.search(text, pos=start_idx)
            if not m_end:
                continue
            code = text[s.start():m_end.end()].strip() + "\n"
            snippets[name] = code
    return snippets

def find_target_files():
    targets = []
    for d in TARGET_DIRS:
        for root, dirs, files in os.walk(d):
            for f in files:
                if f.endswith(".py"):
                    path = os.path.join(root, f)
                    with open(path, "r", encoding="utf-8") as fh:
                        txt = fh.read()
                        if "AUTO_SNIPPETS_ZONE_START" in txt and "AUTO_SNIPPETS_ZONE_END" in txt:
                            targets.append(path)
    return targets

def parse_zone(txt):
    start = txt.find("AUTO_SNIPPETS_ZONE_START")
    end = txt.find("AUTO_SNIPPETS_ZONE_END")
    if start == -1 or end == -1 or end < start:
        return None
    zone_start_idx = txt.find("\n", start) + 1
    zone_end_idx = txt.rfind("\n", 0, end)
    before = txt[:zone_start_idx]
    zone = txt[zone_start_idx:zone_end_idx]
    after = txt[zone_end_idx:]
    return before, zone, after

def get_inserted_snippets(zone_text):
    inserted = {}
    for m in SNIPPET_HEADER.finditer(zone_text):
        name = m.group(1).strip()
        start_idx = m.end()
        m_end = SNIPPET_END.search(zone_text, pos=start_idx)
        if not m_end:
            continue
        code = zone_text[m.start():m_end.end()].strip() + "\n"
        inserted[name] = code
    return inserted

def write_zone_to_file(path, before, zone_text, after):
    new_text = before + zone_text + after
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)

def choose_action_and_apply(snippets, targets):
    if not targets:
        return "No targets with snippet zones found."
    target = random.choice(targets)
    with open(target, "r", encoding="utf-8") as fh:
        txt = fh.read()
    parsed = parse_zone(txt)
    if not parsed:
        return f"No valid zone in {target}"
    before, zone, after = parsed
    inserted = get_inserted_snippets(zone)

    # Удаление
    do_delete = random.random() < PROB_DELETE and inserted
    if do_delete:
        name = random.choice(list(inserted.keys()))
        new_zone = zone.replace(inserted[name], "")
        write_zone_to_file(target, before, new_zone, after)
        return f"Deleted snippet '{name}' from {os.path.relpath(target, ROOT)}"

    # Добавление / замена
    do_add = random.random() < PROB_ADD
    if do_add:
        name, code = random.choice(list(snippets.items()))
        if name in inserted:
            new_zone = zone.replace(inserted[name], code)
            action = "Replaced"
        else:
            new_zone = zone.strip() + "\n\n" + code
            action = "Added"
        write_zone_to_file(target, before, new_zone, after)
        return f"{action} snippet '{name}' into {os.path.relpath(target, ROOT)}"

    # Пустая правка (для активности)
    new_zone = zone + f"\n# autosave {datetime.utcnow().isoformat()}\n"
    write_zone_to_file(target, before, new_zone, after)
    return f"Touched zone in {os.path.relpath(target, ROOT)} (no snippet change)"

def check_syntax():
    """Проверяем, что весь проект компилируется"""
    try:
        py_files = [os.path.join(r, f) for r, d, files in os.walk(ROOT) for f in files if f.endswith(".py")]
        subprocess.run(["python3", "-m", "py_compile"] + py_files, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def git_commit_and_push(message: str):
    try:
        subprocess.run(["git", "add", "."], check=True)
        # если нет изменений, commit вернёт код != 0
        result = subprocess.run(["git", "commit", "-m", message])
        if result.returncode != 0:
            return False, "No changes to commit"
        # всегда тянем свежак с GitHub
        subprocess.run(["git", "pull", "--rebase"], check=True)
        subprocess.run(["git", "push"], check=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, str(e)

def main():
    snippets = load_all_snippets()
    if not snippets:
        notify("No snippets loaded.")
        return
    targets = find_target_files()
    msg = choose_action_and_apply(snippets, targets)

    if not check_syntax():
        notify(f"Syntax error after change: {msg}. Commit aborted.")
        return

    success, err = git_commit_and_push(msg)
    if success:
        notify(f"Committed: {msg}")
    else:
        notify(f"Commit failed: {msg}. Error: {err}")

if __name__ == "__main__":
    main()
