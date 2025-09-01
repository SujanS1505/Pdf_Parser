from src.parser.pdf_parser import PdfParser
from src.parser.normalize import normalize_whitespace, normalize_section_id


def find_toc(pdf_path: str, search_pages: int = 50):
    """
    Look for a 'Table of Contents' section within the first `search_pages`.
    Returns start_page, end_page, lines.
    """
    parser = PdfParser(pdf_path)
    lines = []

    for page_num in range(min(search_pages, parser.get_num_pages())):
        text = parser.extract_text(page_num)
        if not text:
            continue

        for line in text.splitlines():
            clean = normalize_whitespace(line)
            if clean.lower().startswith("table of contents"):
                return page_num, page_num + 5, text.splitlines()

    return None, None, lines


def parse_toc_lines(lines, doc_title: str):
    """
    Parse TOC lines into structured entries.
    """
    toc_entries = []

    for line in lines:
        clean = normalize_whitespace(line)
        if not clean or not clean[0].isdigit():
            continue

        parts = clean.rsplit(" ", 1)  # split title and page number
        if len(parts) == 2 and parts[1].isdigit():
            section_id_title, page = parts
            section_parts = section_id_title.split(" ", 1)
            section_id = normalize_section_id(section_parts[0])
            title = section_parts[1] if len(section_parts) > 1 else ""
            toc_entries.append({
                "section_id": section_id,
                "title": title,
                "page": int(page)
            })

    return toc_entries
