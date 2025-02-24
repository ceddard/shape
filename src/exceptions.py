class MissingEnvironmentVariableError(Exception):
    def __init__(self, variable_name):
        self.variable_name = variable_name
        super().__init__(f"Missing required environment variable: {variable_name}")


class SparkInitializationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class UnknownTraceabilityTypeError(Exception):
    def __init__(self, traceability_type):
        self.traceability_type = traceability_type
        super().__init__(f"Unknown traceability type: {traceability_type}")


class TraceabilityNotImplementedError(Exception):
    def __init__(self, traceability_type):
        self.traceability_type = traceability_type
        super().__init__(f"{traceability_type} is not implemented yet")


class PipelineFailed(Exception):
    def __init__(self, error):
        self.error = error
        super().__init__(f"Pipeline failed: {error}")


# todo: verifique se e necesario self.var = var nas classes
