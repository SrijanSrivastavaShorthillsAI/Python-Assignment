from typing import List, Dict, Any
from PyPDF2 import PdfReader
from loader.file_loader import FileLoader
import re

class DataExtractor:
    def __init__(self, loader: FileLoader):
        self.loader = loader
        self.file = None

    def load(self, file_path: str):
        """Load the file using the provided loader."""
        self.file = self.loader.load_file(file_path)

    def extract_text(self) -> List[Dict[str, Any]]:
        """
        Extract text along with metadata : page numbers, font styles, and headings.
        """
        extracted_data = []
        if isinstance(self.file, PdfReader):  # For PDF (PyPDF2 returns a PdfReader object)
            for page_num, page in enumerate(self.file.pages, start=1):
                # In newer PyPDF2 versions, use `extract_text()`
                text = page.extract_text()
                headings = self._extract_headings(text)
                font_styles = self._extract_font_styles(text)
                extracted_data.append({
                    "page_number": page_num,
                    "text": text,
                    "headings": headings,
                    "font_styles": font_styles
                })
        return extracted_data

    def _extract_headings(self, text: str) -> List[str]:
        """Extract headings from the text based on simple heuristic (e.g., line length or font size)."""
        # assumption: Headings are lines in uppercase or certain length
        headings = [line.strip() for line in text.splitlines() if line.isupper() or len(line) > 30]
        return headings

    def _extract_font_styles(self, text: str) -> Dict[str, int]:
        styles = {'bold': text.lower().count('bold'), 'italic': text.lower().count('italic')}
        return styles

    def extract_links(self) -> List[Dict[str, Any]]:
        """
        Extract hyperlinks along with metadata : linked text, URL, and page/slide number.
        """
        extracted_links = []
        for page_num, page in enumerate(self.file.pages, start=1):
            text = page.extract_text()
            links = re.findall(r'(https?://[^\s]+)', text)
            for link in links:
                extracted_links.append({
                    "linked_text": link,
                    "url": link,
                    "page_number": page_num
                })
        return extracted_links

    def extract_images(self):
        """
        to be implemented
        """
        # raise NotImplementedError("Image extraction requires additional libraries such as pdf2image.")

    def extract_tables(self):
        """
        to be implemented
        """
        raise NotImplementedError("Table extraction requires libraries like camelot or tabula-py.")
