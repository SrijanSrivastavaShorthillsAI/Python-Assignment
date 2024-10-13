import abc
from typing import Any

class FileLoader(abc.ABC):
    @abc.abstractmethod
    def validate(self, file_path: str) -> bool:
        """Validate the file format."""
        pass

    @abc.abstractmethod
    def load_file(self, file_path: str) -> Any:
        """Load and return the file object."""
        pass
