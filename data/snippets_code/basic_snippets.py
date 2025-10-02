# --- snippet: reverse_text ---
def reverse_text(s: str) -> str:
    """
    Reverses text.
    """
    return s[::-1]
# --- endsnippet ---

# --- snippet: count_words ---
def count_words(s: str) -> int:
    """
    Counts words separated by whitespace.
    """
    return len(s.split())
# --- endsnippet ---

# --- snippet: to_title_case ---
def to_title_case(s: str) -> str:
    """
    Make each word start with uppercase.
    """
    return " ".join(w.capitalize() for w in s.split())
# --- endsnippet ---
