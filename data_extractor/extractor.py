from typing import List, Dict, Any
import abc
from loader.file_loader import FileLoader

class DataExtractor(abc.ABC):
    def __init__(self, loader: FileLoader):
        self.loader = loader
        self.file = None
        self.file_path = None

    def load(self, file_path: str):
        """Load the file using the appropriate loader based on file type."""
        self.file = self.loader.load_file(file_path)
        self.file_path = file_path 

    # * for text
    @abc.abstractmethod
    def extract_text(self) -> List[Dict[str, Any]]:
        pass

    # * for heading
    @abc.abstractmethod
    def extract_headings(self, text: str) -> List[str]:
        pass

    # * for font styles
    @abc.abstractmethod
    def extract_font_styles(self) -> Dict[str, int]:
        pass

    # * for images
    @abc.abstractmethod
    def extract_images(self, output_folder: str) -> List[str]:
        pass

    # * for links
    @abc.abstractmethod
    def extract_links(self) -> List[Dict[str, Any]]:
        pass

    # * for tables
    @abc.abstractmethod
    def extract_tables(self, output_folder: str) -> List[str]:
        pass