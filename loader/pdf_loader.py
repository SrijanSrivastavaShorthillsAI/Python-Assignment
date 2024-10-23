from PyPDF2 import PdfReader
from .file_loader import FileLoader

class PDFLoader(FileLoader):
    def load_file(self, file_path: str) -> PdfReader:
        return PdfReader(file_path)

