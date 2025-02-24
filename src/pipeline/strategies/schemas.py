from abc import ABC, abstractmethod
from typing import Any


class PipelineStrategy(ABC):
    @abstractmethod
    def fit_transform(self, data: Any) -> Any:
        pass
