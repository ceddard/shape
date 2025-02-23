from abc import ABC, abstractmethod

class TraceabilitySchema(ABC):
    @abstractmethod
    def start_run(self):
        pass

    @abstractmethod
    def end_run(self):
        pass

    @abstractmethod
    def log_params(self, params):
        pass

    @abstractmethod
    def log_metrics(self, metrics):
        pass

    @abstractmethod
    def log_model(self, model, input_example):
        pass

    @abstractmethod
    def get_run_info(self):
        pass
