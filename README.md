# USB PD Specification Parser

A **Python-based parsing toolkit** to extract structured data from **PDFS**.  

This tool helps engineers and researchers by automatically extracting:  
- 📑 **Table of Contents (TOC)**  
- 📘 **Section headings** from the body  
- 📝 **Metadata** (title, pages, filename)  


Outputs are provided in **JSONL** formats for easy downstream use.

---

## 🚀 Quickstart

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```
### 2. Run Locally
```bash
# We test this locally to check whether it runs smoothly
# Also it generates three json files as output. That is usb_pd_metadata.json, usb_pd_spec.json and usb_pd_toc.json

python app.py "E:\new projects\Pdf_Parser\docs\USB_PD_R3.pdf"

# run this with you current pdf path present in your root directory

```
### 3. Upload pdf via user interface
```
# Run the app
python -m app

# Now the backend runs. After this use the go live option to actually access the frontend so that we can upload the PDFs





