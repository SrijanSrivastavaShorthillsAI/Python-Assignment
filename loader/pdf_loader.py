from PyPDF2 import PdfReader
from .file_loader import FileLoader

class PDFLoader(FileLoader):
    def validate(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pdf')

    def load_file(self, file_path: str) -> PdfReader:
        if not self.validate(file_path):
            raise ValueError("Invalid PDF file.")
        return PdfReader(file_path)

