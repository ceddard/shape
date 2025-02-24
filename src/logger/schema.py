from abc import ABC, abstractmethod


class LogSchema(ABC):
    """
    Abstract class for logging messages.
    implements the log_failure, log_run_info, and log_success
    methods that must be implemented by subclasses.
    """

    @abstractmethod
    def log_failure(self, **kwargs):
        """Log a failure message."""
        pass

    @abstractmethod
    def log_run_info(self, **kwargs):
        """Log run information."""
        pass

    @abstractmethod
    def log_success(self, **kwargs):
        """Log a success message."""
        pass
