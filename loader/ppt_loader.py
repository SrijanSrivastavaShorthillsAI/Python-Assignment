from pptx import Presentation
from .file_loader import FileLoader

class PPTLoader(FileLoader):
    def validate(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pptx')

    def load_file(self, file_path: str) -> Presentation:
        if not self.validate(file_path):
            raise ValueError("Invalid PPT file.")
        return Presentation(file_path)
