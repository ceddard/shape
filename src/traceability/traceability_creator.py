from traceability.services.mlflow import MLflowTraceability

# from traceability.implementations.dvc import DVCTraceability  # descomente quando DVCTraceability for implementado
# from traceability.implementations.biases import BiasesTraceability  # descomente quando BiasesTraceability for implementado
from exceptions import UnknownTraceabilityTypeError, TraceabilityNotImplementedError


class Traceability:
    """
    Traceability class for creating traceability objects.
    """
    _traceability_classes = {
        "mlflow": MLflowTraceability,
        #'dvc': DVCTraceability,
        #'biases': WeightsBiasesTraceability
    }

    def create_traceability(traceability_type):
        """
        Create a traceability object.
        
        Args:
            traceability_type (str): The type of traceability object to create.
        
        raises:
            UnknownTraceabilityTypeError: If the traceability_type is not recognized.
            TraceabilityNotImplementedError: If the traceability_type is recognized but not implemented.
        """
        try:
            return Traceability._traceability_classes[traceability_type]()
        except KeyError:
            raise UnknownTraceabilityTypeError(traceability_type)
        except NotImplementedError:
            raise TraceabilityNotImplementedError(traceability_type)
