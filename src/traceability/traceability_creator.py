from traceability.services.mlflow import MLflowTraceability
# from traceability.implementations.dvc import DVCTraceability  # descomente quando DVCTraceability for implementado
# from traceability.implementations.biases import BiasesTraceability  # descomente quando BiasesTraceability for implementado

class Traceability:
    _traceability_classes = {
        'mlflow': MLflowTraceability,
        #'dvc': DVCTraceability,
        #'biases': WeightsBiasesTraceability
    }

    def create_traceability(traceability_type):
        try:
            return Traceability._traceability_classes[traceability_type]()
        except KeyError:
            raise ValueError(f"Unknown traceability type: {traceability_type}")
        except NotImplementedError:
            raise NotImplementedError(f"{traceability_type} is not implemented yet")