from PyPDF2 import PdfReader
from .file_loader import FileLoader

class PDFLoader(FileLoader):
    def validate(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pdf')
    
    def is_pdf_valid(self, file_path: str) -> bool:
        try:
            with open(file_path, 'rb') as file:
                PdfReader(file)
                return True
        except Exception:
            return False
 
    def load_file(self, file_path: str) -> PdfReader:
        if not self.validate(file_path):
            raise ValueError("Invalid PDF file.")
        if not self.is_pdf_valid(file_path):
            raise ValueError("Corrupted PDF file.")
        return PdfReader(file_path)

