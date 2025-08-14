# USB PD Specification Parsing & Structuring (Starter Kit)

This starter kit parses the USB PD specification PDF to:
- Extract the Table of Contents (TOC)
- Extract section headings from the body
- Emit JSONL files: `usb_pd_toc.jsonl`, `usb_pd_spec.jsonl`, `usb_pd_metadata.jsonl`
- Produce a validation workbook: `validation_report.xlsx`

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m src.main \
  --pdf "/path/to/USB_PD_R3_2 V1.1 2024-10.pdf" \
  --outdir ./out
```

Artifacts are written to `./out`.

## Files

- `src/main.py` — CLI entrypoint
- `src/toc.py` — TOC parsing (pdfminer.six)
- `src/sections.py` — Body headings parsing
- `src/validate.py` — Validation report (Excel) + consistency checks
- `src/schemas.py` — JSON Schemas and helpers
- `src/utils.py` — Common utilities (page extraction, cleaning, writers)

## Notes

- The parser uses heuristics tuned for the USB PD spec (dot leaders, numeric section ids).
- If the PDF has copy-protection or unusual fonts, text extraction might degrade; adjust the heuristics in `toc.py` and `sections.py`.
