from abc import ABC, abstractmethod
from typing import Any


class PipelineStrategy(ABC):
    """
    Abstract class for pipeline strategies.
    methods that must be implemented by subclasses.
    """
    @abstractmethod
    def fit_transform(self, data: Any) -> Any:
        pass
