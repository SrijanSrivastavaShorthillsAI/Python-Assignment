import docx
from .file_loader import FileLoader

class DOCXLoader(FileLoader):
    def load_file(self, file_path: str) -> docx.Document:
        return docx.Document(file_path)
