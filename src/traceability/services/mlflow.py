import mlflow
from mlflow.models import infer_signature
from traceability.schema import TraceabilitySchema
from typing import Dict, Any

class MLflowTraceability(TraceabilitySchema):
    def start_run(self) -> str:
        try:
            mlflow.start_run()
            run_id = mlflow.active_run().info.run_id
            return run_id
        except Exception as e:
            raise RuntimeError(f"Failed to start MLflow run: {str(e)}")

    def end_run(self) -> None:
        try:
            mlflow.end_run()
        except Exception as e:
            raise RuntimeError(f"Failed to end MLflow run: {str(e)}")

    def log_params(self, params: Dict[str, Any]) -> None:
        try:
            for key, value in params.items():
                mlflow.log_param(key, value)
        except Exception as e:
            raise RuntimeError(f"Failed to log MLflow params: {str(e)}")

    def log_metrics(self, metrics: Dict[str, float]) -> None:
        try:
            for key, value in metrics.items():
                mlflow.log_metric(key, value)
        except Exception as e:
            raise RuntimeError(f"Failed to log MLflow metrics: {str(e)}")

    def log_model(self, model: Any, input_example: Any) -> None:
        try:
            signature = infer_signature(input_example)
            mlflow.sklearn.log_model(model, "model", signature=signature)
        except Exception as e:
            raise RuntimeError(f"Failed to log MLflow model: {str(e)}")

    def log_artifact(self, artifact_dict: Dict[str, str]) -> None:
        try:
            for address, file_path in artifact_dict.items():
                mlflow.log_artifact(file_path, artifact_path=address)
        except Exception as e:
            raise RuntimeError(f"Failed to log MLflow artifact: {str(e)}")

    @staticmethod
    def get_run_info() -> Dict[str, Any]:
        try:
            run_info = {
                "run_id": mlflow.active_run().info.run_id,
                "params": mlflow.active_run().data.params,
                "metrics": mlflow.active_run().data.metrics,
                "tags": mlflow.active_run().data.tags
            }
            return run_info
        except Exception as e:
            raise RuntimeError(f"Failed to get MLflow run info: {str(e)}")
