import re

def normalize_whitespace(text: str) -> str:
    """Remove extra spaces, tabs, and newlines."""
    return re.sub(r"\s+", " ", text).strip()

def normalize_section_id(section_id: str) -> str:
    """Standardize section identifiers like '6.1.2'."""
    return section_id.strip().replace(" ", "")

def clean_title(title: str) -> str:
    """Clean and format section titles."""
    return title.strip().capitalize()
