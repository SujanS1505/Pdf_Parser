import re
from typing import List, Dict, Tuple
from .utils import clean, extract_pages_text

TOC_RE_1 = re.compile(r"^\s*(\d+(?:\.\d+)*)\s+(.+?)\s+(\d{1,4})\s*$")
TOC_RE_2 = re.compile(r"^\s*(\d+(?:\.\d+)*)\s+(.+?)\s+\.{2,}\s*(\d{1,4})\s*$")

def find_toc(pdf_path: str, search_pages: int = 80) -> Tuple[int, int, List[str]]:
    pages = extract_pages_text(pdf_path, list(range(search_pages)))
    start = -1
    for i, txt in enumerate(pages):
        if re.search(r"\bTable Of Contents\b|\bTABLE OF CONTENTS\b", txt, re.I):
            start = i; break
    if start < 0:
        return -1, -1, []

    end = start
    lines: List[str] = []
    for j in range(start, min(start + 20, len(pages))):
        txt = pages[j]
        lines.extend(txt.splitlines())
        if re.search(r"\bList of Figures\b", txt, re.I) or re.search(r"^\s*1\s+Introduction\b", txt, re.M):
            end = j
            break
    # normalize
    lines = [clean(l) for l in lines]
    return start, end, lines

def parse_toc_lines(lines: List[str], doc_title: str) -> List[Dict]:
    entries: List[Dict] = []
    for raw in lines:
        line = clean(raw)
        m = TOC_RE_1.match(line) or TOC_RE_2.match(line)
        if not m:
            continue
        sid, title, page = m.group(1), m.group(2), int(m.group(3))
        title = re.sub(r"(\.\s*){2,}", " ", title).strip(" .")
        level = len(sid.split("."))
        parent = ".".join(sid.split(".")[:-1]) if "." in sid else None
        entries.append({
            "doc_title": doc_title,
            "section_id": sid,
            "title": title,
            "full_path": f"{sid} {title}",
            "page": page,
            "level": level,
            "parent_id": parent,
            "tags": []
        })
    return entries
