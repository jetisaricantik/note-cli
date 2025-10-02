# --- snippet: unique_words_sorted ---
def unique_words_sorted(text: str) -> list:
    """
    Returns sorted list of unique words.
    """
    s = set(w.strip('.,!?()[]') for w in text.split())
    return sorted(w for w in s if w)
# --- endsnippet ---

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

# --- snippet: find_anagrams ---
from collections import defaultdict
def find_anagrams(words: list[str]) -> dict:
    """
    Group words into anagrams.
    """
    groups = defaultdict(list)
    for w in words:
        key = "".join(sorted(w.lower()))
        groups[key].append(w)
    return {k: v for k, v in groups.items() if len(v) > 1}
# --- endsnippet ---
