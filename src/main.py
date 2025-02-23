import datetime
import json
import os
import time
import numpy as np
from loader.load import Load
from pipeline.builder import PipelineBuilder
from logger.kafka_logger import KafkaFacade
from utils import save_metrics_to_json, save_to_postgres, convert_keys  # Import the convert_keys function
from config import settings
from engine.spark_engine import SparkEngine
from traceability.provider_traceability import Traceability
from pipeline.pipeline import PipelineHandler

spark_engine = SparkEngine()  # Default
spark = spark_engine.spark #rever implementacao futura
traceability = Traceability.create_traceability("mlflow")  # Default, mover no futuro
logger = KafkaFacade()  # TODO: mover para o construtor do pacote


def score():
    try:
        run_id = traceability.start_run()  # TODO: modularizar para tracebality e criar excessao, ou rever implementacao futura
        timestamp = datetime.datetime.now().isoformat()  # TODO: modularizar para utils, ou rever implementacao futura
        
        pipeline_handler = PipelineHandler()
        predictions, metrics, result, data = pipeline_handler.get_predictions_and_metrics()

        traceability.log_params({
            "data_shape": metrics["data_shape"],
            "transformed_data_shape": metrics["transformed_data_shape"]
        })
        traceability.log_metrics({
            "unique_predictions": metrics["unique_predictions"]
        })

        input_example = data[:5]
        transformed_input_example = pipeline_handler.pipeline.fit_transform(input_example)
        traceability.log_model(pipeline_handler.load.model, transformed_input_example)

        success_message = 'Model scored successfully'
        logger.log_success(message=success_message)

        metrics_file_path = os.path.join('logs', 'metrics.json')
        save_metrics_to_json(metrics, metrics_file_path)

        traceability_info = traceability.get_run_info()
        save_to_postgres(run_id, timestamp, predictions.tolist(), result, data.tolist(), traceability_info)

        logger.log_run_info(
            run_id=run_id,
            timestamp=timestamp,
            predictions=convert_keys(predictions.tolist()),
            result=convert_keys(result),
            data=convert_keys(data.tolist()),
            mlflow_info=convert_keys(traceability_info)
        )

        return {
            "predictions": predictions,
            "summary": result
        }
    except Exception as error:
        print(error)
        logger.log_failure(error=error)
        return None
    finally:
        traceability.end_run()

if __name__ == '__main__':
    result = score()
    if result:
        print("Predictions:", result["predictions"])
        print("Summary:", result["summary"])
    
    print("Spark UI disponível. Pressione Ctrl+C para sair.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando SparkContext...")
        spark_engine.stop_spark_session()
