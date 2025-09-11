from flask import Flask, request, jsonify
from flask_cors import CORS
import os, tempfile, sys, json

from src.parser.pdf_parser import PdfParser
from src.toc import find_toc, parse_toc_lines
from src.sections import parse_body_sections

app = Flask(__name__)
CORS(app)  # allow frontend requests


def process_pdf(pdf_path: str, start_page: int = 1, end_page: int = None):
    """
    Core parser function used by both Flask and CLI.
    Returns a dict with metadata, toc, and sections.
    """
    parser = PdfParser(pdf_path)
    doc_title = parser.extract_metadata().get("/Title", "Untitled Document")

    total_pages = parser.get_num_pages()
    if end_page is None or end_page > total_pages:
        end_page = total_pages

    # TOC
    toc_start, toc_end, toc_lines = find_toc(pdf_path, search_pages=120)
    toc_entries = parse_toc_lines(toc_lines, doc_title=doc_title)

    # Sections
    body_entries = parse_body_sections(
        pdf_path,
        start_page=start_page,
        end_page=end_page,
        doc_title=doc_title
    )

    # Merge TOC pages into body entries
    page_by_id = {e["section_id"]: e["page"] for e in toc_entries}
    for b in body_entries:
        if b.get("page") is None and b["section_id"] in page_by_id:
            b["page"] = page_by_id[b["section_id"]]

    return {
        "metadata": {
            "doc_title": doc_title,
            "file_name": os.path.basename(pdf_path),
            "total_pages": total_pages,
            "parsed_range": f"{start_page} - {end_page}"
        },
        "toc": toc_entries,
        "sections": body_entries,
    }


@app.route("/parse-pdf", methods=["POST"])
def parse_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    tmp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(tmp_dir, file.filename)
    file.save(pdf_path)

    try:
        start_page = int(request.form.get("start_page", 1))
        end_page = int(request.form.get("end_page")) if request.form.get("end_page") else None
    except ValueError:
        return jsonify({"error": "Invalid start or end page"}), 400

    result = process_pdf(pdf_path, start_page, end_page)
    return jsonify(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # CLI mode
        pdf_path = sys.argv[1]
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        result = process_pdf(pdf_path)

        # Save JSON files
        with open(os.path.join(output_dir, "usb_pd_metadata.json"), "w", encoding="utf-8") as f:
            json.dump(result["metadata"], f, indent=2)

        with open(os.path.join(output_dir, "usb_pd_toc.json"), "w", encoding="utf-8") as f:
            json.dump(result["toc"], f, indent=2)

        with open(os.path.join(output_dir, "usb_pd_spec.json"), "w", encoding="utf-8") as f:
            json.dump(result["sections"], f, indent=2)

        print(f"✅ Metadata, TOC, and Sections saved in {output_dir}/")
    else:
        # Flask mode
        app.run(debug=True)
