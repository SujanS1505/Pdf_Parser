import re


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in a string."""
    return " ".join(text.split())


def normalize_section_id(text: str) -> str:
    """Normalize section ID (e.g., '1.2.3')."""
    return re.sub(r"[^0-9.]", "", text)
