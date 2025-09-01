from PyPDF2 import PdfReader


class PdfParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.reader = PdfReader(file_path)

    def get_num_pages(self) -> int:
        """Return total number of pages in the PDF."""
        return len(self.reader.pages)

    def extract_text(self, page_number: int) -> str:
        """Extract plain text from a given page (0-based index)."""
        if page_number < 0 or page_number >= self.get_num_pages():
            raise IndexError("Page number out of range")
        return self.reader.pages[page_number].extract_text()

    def extract_metadata(self) -> dict:
        """Extract PDF metadata (title, author, etc.)."""
        metadata = self.reader.metadata
        return {key: str(value) for key, value in metadata.items()}
