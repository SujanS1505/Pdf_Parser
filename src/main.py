import argparse, os, re, json
from typing import List, Dict
from .utils import write_jsonl, extract_pages_text
from .toc import find_toc, parse_toc_lines
from .sections import parse_body_sections
from .schemas import TOC_SCHEMA, SPEC_SCHEMA, META_SCHEMA
from jsonschema import validate

def detect_title(pdf_path: str) -> str:
    first = extract_pages_text(pdf_path, [0])[0]
    m = re.search(
        r"Universal Serial Bus\s+Power Delivery Specification.*?Revision\s*:?\s*([0-9.]+).*?Version\s*:?\s*([0-9.]+).*?Release Date:\s*([0-9-]+)",
        first, re.S | re.I
    )
    if m:
        return f"USB Power Delivery Specification, Revision {m.group(1)}, Version {m.group(2)} ({m.group(3)})"
    return "USB Power Delivery Specification"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="Path to USB PD PDF")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--body-start", type=int, default=40)
    ap.add_argument("--body-end", type=int, default=300)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    doc_title = detect_title(args.pdf)

    # 1) TOC extraction
    toc_start, toc_end, toc_lines = find_toc(args.pdf, search_pages=120)
    toc_entries: List[Dict] = parse_toc_lines(toc_lines, doc_title=doc_title)

    # Remove "page" key if exists
    for entry in toc_entries:
        entry.pop("page", None)

    # 2) Body extraction
    body_entries: List[Dict] = parse_body_sections(
        args.pdf,
        start_page=args.body_start,
        end_page=args.body_end,
        doc_title=doc_title
    )

    for entry in body_entries:
        entry.pop("page", None)

    # 3) Write TOC & spec outputs
    toc_path = os.path.join(args.outdir, "usb_pd_toc.jsonl")
    spec_path = os.path.join(args.outdir, "usb_pd_spec.jsonl")
    write_jsonl(toc_path, toc_entries)
    write_jsonl(spec_path, body_entries)

    # 4) Metadata (with num_pdf_pages)
    from PyPDF2 import PdfReader
    reader = PdfReader(args.pdf)
    num_pages = len(reader.pages)

    metadata = {
        "doc_title": doc_title,
        "file_name": os.path.basename(args.pdf),
        "num_pdf_pages": num_pages,
        "toc_page_range": [toc_start + 1, toc_end + 1] if toc_start >= 0 and toc_end >= toc_start else None,
        "parsed_body_page_window": [args.body_start, args.body_end]
    }

    meta_path = os.path.join(args.outdir, "usb_pd_metadata.jsonl")
    write_jsonl(meta_path, [metadata])

    # 5) Validate against JSON Schemas
    for path, schema in [(toc_path, TOC_SCHEMA), (spec_path, SPEC_SCHEMA), (meta_path, META_SCHEMA)]:
        with open(path, "r", encoding="utf-8") as f:
            for ln, line in enumerate(f, 1):
                try:
                    obj = json.loads(line)
                    validate(instance=obj, schema=schema)
                except Exception as e:
                    print(f"[WARN] Schema validation issue in {os.path.basename(path)} line {ln}: {e}")

    # 6) Validation workbook
    from .validate import make_validation_excel
    xlsx_path = os.path.join(args.outdir, "validation_report.xlsx")
    make_validation_excel(xlsx_path, toc_entries, body_entries)

    print("Done. Outputs at:", args.outdir)

if __name__ == "__main__":
    main()
