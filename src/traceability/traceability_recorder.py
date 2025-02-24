from config import settings

class TraceabilityLogger:
    @staticmethod
    def log_traceability_info(traceability, pipeline_handler, metrics, data):
        traceability.log_params({
            "data_shape": metrics["data_shape"],
            "transformed_data_shape": metrics["transformed_data_shape"]
        })
        traceability.log_metrics({
            "unique_predictions": metrics["unique_predictions"]
        })
        traceability.log_artifact({
            "model": settings.ARTIFACT})

        input_example = data[:5]
        transformed_input_example = pipeline_handler.pipeline.fit_transform(input_example)
        traceability.log_model(pipeline_handler.load.model, transformed_input_example)
