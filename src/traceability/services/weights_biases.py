from traceability.schema import Traceability


class WeightsBiasesTraceability(Traceability):
    """
    WeightsBiasesTraceability class for logging
    model training information to Weights & Biases.

    not implemented yet.
    """

    def start_run(self):
        raise NotImplementedError(
            "start_run method is not implemented for "
            "WeightsBiasesTraceability"
        )

    def end_run(self):
        raise NotImplementedError(
            "end_run method is not implemented for "
            "WeightsBiasesTraceability"
        )

    def log_params(self, params):
        raise NotImplementedError(
            "log_params method is not implemented for "
            "WeightsBiasesTraceability"
        )

    def log_metrics(self, metrics):
        raise NotImplementedError(
            "log_metrics method is not implemented for "
            "WeightsBiasesTraceability"
        )

    def log_model(self, model, input_example):
        raise NotImplementedError(
            "log_model method is not implemented for"
            "WeightsBiasesTraceability"
        )

    def get_run_info(self):
        raise NotImplementedError(
            "get_run_info method is not implemented for"
            "WeightsBiasesTraceability"
        )

    def log_artifact(self, artifact_path):
        raise NotImplementedError(
            "log_artifact method is not implemented for"
            "WeightsBiasesTraceability"
        )
