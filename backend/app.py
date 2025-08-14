from flask import Flask, request, send_file, jsonify
import os
import tempfile
import subprocess

app = Flask(__name__, static_folder="../frontend", static_url_path="")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/parse", methods=["POST"])
def parse_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    pdf_file = request.files["pdf"]
    body_start = request.form.get("body_start", "40")
    body_end = request.form.get("body_end", "300")

    temp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(temp_dir, pdf_file.filename)
    pdf_file.save(pdf_path)

    out_dir = os.path.join(temp_dir, "out")
    os.makedirs(out_dir, exist_ok=True)

    subprocess.run([
        "python", "-m", "src.main",
        "--pdf", pdf_path,
        "--outdir", out_dir,
        "--body-start", body_start,
        "--body-end", body_end
    ], check=True)

    files = {f: os.path.join(out_dir, f) for f in os.listdir(out_dir)}
    return jsonify(files)

@app.route("/download", methods=["GET"])
def download_file():
    path = request.args.get("path")
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
