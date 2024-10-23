from pptx import Presentation
from .file_loader import FileLoader

class PPTLoader(FileLoader):
    def load_file(self, file_path: str) -> Presentation:
        return Presentation(file_path)
