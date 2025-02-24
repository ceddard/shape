from config import settings
from typing import Any, Dict


class TraceabilityLogger:
    """
    TraceabilityLogger class for logging
    """
    @staticmethod
    def log_traceability_info(
        traceability: Any, pipeline_handler: Any, metrics: Dict[str, Any], data: Any
    ) -> None:
        """
        Log traceability information.
        
        Args:
            traceability (Any): The traceability object.
            pipeline_handler (Any): The pipeline handler object.
            metrics (Dict[str, Any]): The metrics information.
            data (Any): The data object.
        """
        traceability.log_params(
            {
                "data_shape": metrics["data_shape"],
                "transformed_data_shape": metrics["transformed_data_shape"],
            }
        )
        traceability.log_metrics({"unique_predictions": metrics["unique_predictions"]})
        traceability.log_artifact({"model": settings.ARTIFACT})

        input_example = data.limit(5).collect()
        transformed_input_example = pipeline_handler.pipeline.fit_transform(
            input_example
        )
        traceability.log_model(pipeline_handler.load.model, transformed_input_example)
