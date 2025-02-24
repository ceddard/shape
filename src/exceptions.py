class MissingEnvironmentVariableError(Exception):
    """
    Custom exception for missing environment variables.
    """

    def __init__(self, variable_name):
        self.variable_name = variable_name
        super().__init__(
            f"Missing required environment variable: {variable_name}")


class SparkInitializationError(Exception):
    """
    Custom exception for Spark initialization error.
    """

    def __init__(self, message):
        super().__init__(message)


class UnknownTraceabilityTypeError(Exception):
    """
    Custom exception for unknown traceability type.
    """

    def __init__(self, traceability_type):
        self.traceability_type = traceability_type
        super().__init__(f"Unknown traceability type: {traceability_type}")


class TraceabilityNotImplementedError(Exception):
    """
    Custom exception for traceability not implemented yet.
    """

    def __init__(self, traceability_type):
        self.traceability_type = traceability_type
        super().__init__(f"{traceability_type} is not implemented yet")


class PipelineFailed(Exception):
    """
    Custom exception for pipeline failure.
    """

    def __init__(self, error):
        self.error = error
        super().__init__(f"Pipeline failed: {error}")


class RuntimeFailed(RuntimeError):
    """
    Custom runtime error for handling specific runtime exceptions.
    """

    def __init__(self, message):
        super().__init__(message)
