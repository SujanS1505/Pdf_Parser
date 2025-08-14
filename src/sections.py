import re
from typing import List, Dict
from .utils import clean, extract_pages_text

HEAD_RE = re.compile(r"^\s*(\d+(?:\.\d+)+)\s+([^\n]+?)\s*$", re.M)

def parse_body_sections(pdf_path: str, start_page: int = 40, end_page: int = 300, doc_title: str = "") -> List[Dict]:
    idxs = list(range(start_page, end_page))
    pages = extract_pages_text(pdf_path, idxs)
    rows: List[Dict] = []
    seen = set()
    for rel, txt in enumerate(pages):
        abs_idx = start_page + rel
        for m in HEAD_RE.finditer(txt):
            sid, title = m.group(1), clean(m.group(2))
            title = re.sub(r"\s*Page\s+\d+\s*$", "", title).strip(" .")
            key = (sid, abs_idx)
            if key in seen:
                continue
            seen.add(key)
            level = len(sid.split("."))
            parent = ".".join(sid.split(".")[:-1]) if "." in sid else None
            rows.append({
                "doc_title": doc_title or "USB Power Delivery Specification",
                "section_id": sid,
                "title": title,
                "full_path": f"{sid} {title}",
                "page": None,
                "pdf_page": abs_idx + 1,
                "level": level,
                "parent_id": parent,
                "tags": []
            })
    # dedupe by section_id, keep earliest pdf_page
    best = {}
    for r in rows:
        sid = r["section_id"]
        if sid not in best or r["pdf_page"] < best[sid]["pdf_page"]:
            best[sid] = r
    return list(best.values())
