class SectionNode:
    def __init__(self, section_id: str, title: str, page: int, level: int = 0):
        self.section_id = section_id
        self.title = title
        self.page = page
        self.level = level
        self.children = []

    def add_child(self, child: "SectionNode"):
        """Attach a child node under this section."""
        self.children.append(child)

    def to_dict(self) -> dict:
        """Convert hierarchy into JSON-friendly dict."""
        return {
            "section_id": self.section_id,
            "title": self.title,
            "page": self.page,
            "level": self.level,
            "children": [child.to_dict() for child in self.children]
        }
