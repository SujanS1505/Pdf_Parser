import re, json
from typing import List, Dict
from pdfminer.high_level import extract_text

def clean(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.replace("\xa0", " ").replace("\u200b", " ")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()

def extract_pages_text(pdf_path: str, page_indices: List[int]) -> List[str]:
    out = []
    for i in page_indices:
        try:
            t = extract_text(pdf_path, page_numbers=[i]) or ""
        except Exception:
            t = ""
        out.append(t)
    return out

def write_jsonl(path: str, rows: List[Dict]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
