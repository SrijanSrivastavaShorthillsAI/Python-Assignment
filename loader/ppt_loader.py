from pptx import Presentation
from .file_loader import FileLoader

class PPTLoader(FileLoader):
    def validate(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pptx')
    
    def is_pptx_valid(self, file_path: str) -> bool:
            try:
                Presentation(file_path)
                return True
            except Exception:
                return False

    def load_file(self, file_path: str) -> Presentation:
        if not self.validate(file_path):
            raise ValueError("Invalid PPT file.")
        if not self.is_pptx_valid(file_path):
            raise ValueError("Corrupted PPT file.")
        return Presentation(file_path)
