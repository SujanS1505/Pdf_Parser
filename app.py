from flask import Flask, request, jsonify
from flask_cors import CORS
import os, tempfile
from PyPDF2 import PdfReader   # <-- added

from src.main import detect_title
from src.toc import find_toc, parse_toc_lines
from src.sections import parse_body_sections

app = Flask(__name__)
CORS(app)  # allow frontend requests

@app.route("/parse-pdf", methods=["POST"])
def parse_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded file
    tmp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(tmp_dir, file.filename)
    file.save(pdf_path)

    # Run your parser
    doc_title = detect_title(pdf_path)
    toc_start, toc_end, toc_lines = find_toc(pdf_path, search_pages=120)
    toc_entries = parse_toc_lines(toc_lines, doc_title=doc_title)

    # get total number of pages dynamically
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    # parse the full PDF body (from page 40 to last page)
    body_entries = parse_body_sections(
        pdf_path,
        start_page=40,
        end_page=total_pages,
        doc_title=doc_title
    )

    # Merge TOC pages into body entries
    page_by_id = {e["section_id"]: e["page"] for e in toc_entries}
    for b in body_entries:
        if b.get("page") is None and b["section_id"] in page_by_id:
            b["page"] = page_by_id[b["section_id"]]

    return jsonify({
        "metadata": {
            "doc_title": doc_title,
            "file_name": file.filename,
            "total_pages": total_pages   # <-- added for frontend display
        },
        "toc": toc_entries,
        "sections": body_entries,
    })

if __name__ == "__main__":
    app.run(debug=True)
