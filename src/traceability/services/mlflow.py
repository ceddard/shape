import mlflow
from mlflow.models import infer_signature
from traceability.schema import TraceabilitySchema
from typing import Dict, Any
from exceptions import RuntimeFailed


class MLflowTraceability(TraceabilitySchema):
    """
    MLflowTraceability class for logging
    model training information to MLflow.
    """
    def start_run(self) -> str:
        """
        Start an MLflow run.
        
        Returns:
            str: The run ID of the started MLflow run.

        raises:
            RuntimeFailed: If starting the MLflow run fails.
        """
        try:
            mlflow.start_run()
            run_id = mlflow.active_run().info.run_id
            return run_id
        except Exception as e:
            raise RuntimeFailed(f"Failed to start MLflow run: {str(e)}")

    def end_run(self) -> None:
        """
        End the active MLflow run.

        raises:
            RuntimeFailed: If ending the MLflow run fails.
        """
        try:
            mlflow.end_run()
        except Exception as e:
            raise RuntimeFailed(f"Failed to end MLflow run: {str(e)}")

    def log_params(self, params: Dict[str, Any]) -> None:
        """
        Log parameters to the active MLflow run.
        
        Args:
            params (Dict[str, Any]): The parameters to log.
            
        raises:
            RuntimeFailed: If logging the MLflow params fails.
        """
        try:
            for key, value in params.items():
                mlflow.log_param(key, value)
        except Exception as e:
            raise RuntimeFailed(f"Failed to log MLflow params: {str(e)}")

    def log_metrics(self, metrics: Dict[str, float]) -> None:
        """
        Log metrics to the active MLflow run.
        
        Args:
            metrics (Dict[str, float]): The metrics to log.
            
        raises:
            RuntimeFailed: If logging the MLflow metrics fails.
        """
        try:
            for key, value in metrics.items():
                mlflow.log_metric(key, value)
        except Exception as e:
            raise RuntimeFailed(f"Failed to log MLflow metrics: {str(e)}")

    def log_model(self, model: Any, input_example: Any) -> None:
        """
        Log the model to the active MLflow run.
        
        Args:
            model (Any): The model to log.
            input_example (Any): An example input to infer the model signature.
            
        raises:
            RuntimeFailed: If logging the MLflow model fails.
        """
        try:
            signature = infer_signature(input_example)
            mlflow.sklearn.log_model(model, "model", signature=signature)
        except Exception as e:
            raise RuntimeFailed(f"Failed to log MLflow model: {str(e)}")

    def log_artifact(self, artifact_dict: Dict[str, str]) -> None:
        """
        Log artifacts to the active MLflow run.
        
        Args:
            artifact_dict (Dict[str, str]): The artifacts to log.

        raises:
            RuntimeFailed: If logging the MLflow artifacts fails.
        """
        try:
            for address, file_path in artifact_dict.items():
                mlflow.log_artifact(file_path, artifact_path=address)
        except Exception as e:
            raise RuntimeFailed(f"Failed to log MLflow artifact: {str(e)}")

    @staticmethod
    def get_run_info() -> Dict[str, Any]:
        """
        Get information about the active MLflow run.
        
        Returns:
            Dict[str, Any]: The run information.
            
        raises:
            RuntimeFailed: If getting the MLflow run info fails.
        """
        try:
            run_info = {
                "run_id": mlflow.active_run().info.run_id,
                "params": mlflow.active_run().data.params,
                "metrics": mlflow.active_run().data.metrics,
                "tags": mlflow.active_run().data.tags,
            }
            return run_info
        except Exception as e:
            raise RuntimeFailed(f"Failed to get MLflow run info: {str(e)}")
