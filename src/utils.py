import re, json
from typing import List, Dict
from PyPDF2 import PdfReader

def clean(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.replace("\xa0", " ").replace("\u200b", " ")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()

def extract_pages_text(pdf_path: str, page_indices: List[int]) -> List[str]:
    """Fast text extraction using PyPDF2."""
    out = []
    reader = PdfReader(pdf_path)
    for i in page_indices:
        if i < 0 or i >= len(reader.pages):
            out.append("")
            continue
        try:
            txt = reader.pages[i].extract_text() or ""
        except Exception:
            txt = ""
        out.append(txt)
    return out

def write_jsonl(path: str, rows: List[Dict]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
