from typing import Dict, Any

TOC_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "doc_title": {"type": "string"},
        "section_id": {"type": "string"},
        "title": {"type": "string"},
        "full_path": {"type": "string"},
        "page": {"type": "integer"},
        "level": {"type": "integer"},
        "parent_id": {"type": ["string", "null"]},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["doc_title", "section_id", "title", "full_path", "page", "level", "parent_id"],
    "additionalProperties": True,
}

SPEC_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "doc_title": {"type": "string"},
        "section_id": {"type": "string"},
        "title": {"type": "string"},
        "full_path": {"type": "string"},
        "page": {"type": ["integer", "null"]},
        "pdf_page": {"type": ["integer", "null"]},
        "level": {"type": "integer"},
        "parent_id": {"type": ["string", "null"]},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["doc_title", "section_id", "title", "full_path", "level", "parent_id"],
    "additionalProperties": True,
}

META_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "doc_title": {"type": "string"},
        "file_name": {"type": "string"},
        "num_pdf_pages": {"type": ["integer", "null"]},
        "toc_page_range": {"type": "array"},
        "parsed_body_page_window": {"type": "array"},
    },
    "required": ["doc_title", "file_name"],
    "additionalProperties": True,
}
