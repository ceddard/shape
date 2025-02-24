from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log_failure(self, **kwargs):
        pass

    @abstractmethod
    def log_run_info(self, **kwargs):
        pass

    @abstractmethod
    def log_success(self, **kwargs):
        pass
