from abc import ABC, abstractmethod


class TraceabilitySchema(ABC):
    """
    Abstract class for traceability schema
    methods must be implemented by the subclasses
    """
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

    @abstractmethod
    def log_artifact(self, artifact_path):
        pass
