from src.parser.pdf_parser import PdfParser
from src.parser.normalize import normalize_whitespace, normalize_section_id


def parse_body_sections(pdf_path: str, start_page: int, end_page: int, doc_title: str):
    """
    Parse PDF body pages into structured sections.
    """
    parser = PdfParser(pdf_path)
    sections = []

    for page_num in range(start_page, min(end_page, parser.get_num_pages())):
        text = parser.extract_text(page_num)
        if not text:
            continue

        for line in text.splitlines():
            clean = normalize_whitespace(line)
            if not clean or not clean[0].isdigit():
                continue

            parts = clean.split(" ", 1)
            section_id = normalize_section_id(parts[0])
            title = parts[1] if len(parts) > 1 else ""
            sections.append({
                "section_id": section_id,
                "title": title,
                "page": page_num
            })

    return sections
