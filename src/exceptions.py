class MissingEnvironmentVariableError(Exception):
    def __init__(self, variable_name):
        self.variable_name = variable_name
        super().__init__(f"Missing required environment variable: {variable_name}")

class SparkInitializationError(Exception):
    def __init__(self, message):
        super().__init__(message)
