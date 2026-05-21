from abc import ABC, abstractmethod
from typing import Any, Dict

class Tool(ABC):
    """
    Base class for all agent tools.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "description": self.description
        }
