from abc import ABC, abstractmethod
from typing import Any


class StepStrategy(ABC):
    """
    StepStrategy interface for applying a step configuration
    to a specific step.
    must be implemented by all concrete strategies.
    """

    @abstractmethod
    def apply(self, step_config: dict) -> Any:
        raise NotImplementedError("You should implement this method")
