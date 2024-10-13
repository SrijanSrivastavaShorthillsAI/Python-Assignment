from typing import Any
from storage.storage import Storage
from data_extractor.extractor import DataExtractor

class FileStorage(Storage):
    def __init__(self, extractor: DataExtractor):
        self.extractor = extractor

    def store_data(self, data: Any, file_path: str):
        with open(file_path, 'w') as file:
            file.write(str(data))
