section_schema = {
    "type": "object",
    "properties": {
        "section_id": {"type": "string"},
        "title": {"type": "string"},
        "page": {"type": "integer"}
    },
    "required": ["section_id", "title", "page"]
}

toc_schema = {
    "type": "array",
    "items": section_schema
}
