import docx
from .file_loader import FileLoader

class DOCXLoader(FileLoader):
    def validate(self, file_path: str) -> bool:
        return file_path.lower().endswith('.docx')
    
    def is_docx_valid(self, file_path: str) -> bool:
        try:
            docx.Document(file_path)
            return True
        except Exception:
            return False

    def load_file(self, file_path: str) -> docx.Document:
        if not self.validate(file_path):
            raise ValueError("Invalid DOCX file.")
        if not self.is_docx_valid(file_path):
            raise ValueError("Corrupted DOCX file.")
        return docx.Document(file_path)
