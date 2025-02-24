import mlflow
from traceability.schema import TraceabilitySchema

class MLflowTraceability(TraceabilitySchema):
    def start_run(self):
        try:
            mlflow.start_run()
            run_id = mlflow.active_run().info.run_id
            return run_id
        except Exception as e:
            raise RuntimeError(f"Failed to start MLflow run: {str(e)}")

    def end_run(self):
        try:
            mlflow.end_run
        except Exception as e:
            raise RuntimeError(f"Failed to end MLflow run: {str(e)}")

    def log_params(self, params):
        try:
            for key, value in params.items():
                mlflow.log_param(key, value)
        except Exception as e:
            raise RuntimeError(f"Failed to log MLflow params: {str(e)}")

    def log_metrics(self, metrics):
        try:
            for key, value in metrics.items():
                mlflow.log_metric(key, value)
        except Exception as e:
            raise RuntimeError(f"Failed to log MLflow metrics: {str(e)}")

    def log_model(self, model, input_example):
        try:
            mlflow.sklearn.log_model(model, "model", input_example=input_example)
        except Exception as e:
            raise RuntimeError(f"Failed to log MLflow model: {str(e)}")

    @staticmethod
    def get_run_info():
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
