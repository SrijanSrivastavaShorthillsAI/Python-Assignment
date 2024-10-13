import abc
from typing import Any

class Storage(abc.ABC):
    @abc.abstractmethod
    def store_data(self, data: Any):
        """Store extracted data."""
        pass
