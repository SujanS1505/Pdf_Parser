from flask import Flask, request, jsonify
from flask_cors import CORS
import os, tempfile

from src.parser.pdf_parser import PdfParser
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

    # Save uploaded file temporarily
    tmp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(tmp_dir, file.filename)
    file.save(pdf_path)

    # Initialize parser
    parser = PdfParser(pdf_path)
    doc_title = parser.extract_metadata().get("/Title", "Untitled Document")

    # Get total pages dynamically
    total_pages = parser.get_num_pages()

    # ✅ Get start_page and end_page from frontend
    try:
        start_page = int(request.form.get("start_page", 1))
        end_page = int(request.form.get("end_page", total_pages))
    except ValueError:
        return jsonify({"error": "Invalid start or end page"}), 400

    # Ensure valid ranges
    if start_page < 1 or end_page > total_pages or start_page > end_page:
        return jsonify({"error": f"Invalid page range. Document has {total_pages} pages."}), 400

    # Find TOC
    toc_start, toc_end, toc_lines = find_toc(pdf_path, search_pages=120)
    toc_entries = parse_toc_lines(toc_lines, doc_title=doc_title)

    # Extract body sections for requested page range
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

    return jsonify({
        "metadata": {
            "doc_title": doc_title,
            "file_name": file.filename,
            "total_pages": total_pages,
            "parsed_range": f"{start_page} - {end_page}"
        },
        "toc": toc_entries,
        "sections": body_entries,
    })


if __name__ == "__main__":
    app.run(debug=True)
