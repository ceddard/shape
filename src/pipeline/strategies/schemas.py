from abc import ABC, abstractmethod

class PipelineStrategy(ABC):
    @abstractmethod
    def fit_transform(self, data):
        pass
