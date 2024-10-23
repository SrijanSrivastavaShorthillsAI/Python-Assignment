import abc
from typing import Any

class FileLoader(abc.ABC):
    @abc.abstractmethod
    def load_file(self, file_path: str) -> Any:
        """Load and return the file object."""
        pass
