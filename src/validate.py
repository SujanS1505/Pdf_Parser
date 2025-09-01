from src.parser.normalize import normalize_whitespace


def validate_section(entry: dict) -> bool:
    """Check if a parsed section entry is valid."""
    if not entry.get("section_id") or not entry.get("title"):
        return False
    return True


def validate_toc(toc_entries: list) -> bool:
    """Validate that TOC entries are not empty and normalized."""
    return all("section_id" in e and "title" in e for e in toc_entries)
