from abc import ABC, abstractmethod
from typing import Any


class StepStrategy(ABC):
    @abstractmethod
    def apply(self, step_config: dict) -> Any:
        raise NotImplementedError("You should implement this method")
