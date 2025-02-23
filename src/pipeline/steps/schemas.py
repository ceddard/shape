from abc import ABC, abstractmethod

class StepStrategy(ABC):
    @abstractmethod
    def apply(self, step_config):
        raise NotImplementedError("You should implement this method")
