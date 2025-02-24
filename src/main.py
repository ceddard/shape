import os
import sys
from logger.kafka_logger import Logger
from utils import get_current_timestamp, Converter
from database import postgres_saver  # Import the new class
from database.json import save_metrics_to_json
from engine.spark_engine import SparkEngine
from traceability.traceability_creator import Traceability
from pipeline.pipeline import PipelineHandler
from traceability.traceability_recorder import TraceabilityLogger
from exceptions import PipelineFailed

spark_engine = SparkEngine()  # Default
spark = spark_engine.spark #rever implementacao futura
traceability = Traceability.create_traceability("mlflow")  # Default, mover no futuro
logger = Logger()  # TODO: mover para o construtor do pacote

def score():
    try:
        run_id = traceability.start_run()  # TODO: modularizar para tracebality e criar excessao, ou rever implementacao futura
        timestamp = get_current_timestamp()  # Chame a função diretamente
        
        pipeline_handler = PipelineHandler()
        predictions, metrics, result, data = pipeline_handler.get_predictions_and_metrics()

        TraceabilityLogger.log_traceability_info(traceability, pipeline_handler, metrics, data)

        logger.log_success(message='Model scored successfully')

        metrics_file_path = os.path.join('logs', 'metrics.json')
        save_metrics_to_json(metrics, metrics_file_path)

        traceability_info = traceability.get_run_info()

        postgres_saver.save_to_postgres(run_id, timestamp, predictions.tolist(), result, data.tolist(), traceability_info)  # Pass traceability_info as log_info

        logger.log_run_info( #TODO: verificar conversao.
            run_id=run_id,
            timestamp=timestamp,
            predictions=Converter.convert_keys(predictions.tolist()),
            result=Converter.convert_keys(result),
            data=Converter.convert_keys(data.tolist()),
            mlflow_info=Converter.convert_keys(traceability_info)
        )

        return {
            "predictions": predictions,
            "summary": result
        }
    except Exception as error:
        logger.log_failure(error=error)
        raise PipelineFailed(error)
    finally:
        traceability.end_run()

if __name__ == '__main__':
    result = score()
    sys.stdout.write(str(result))
    
    #if result:
    #    print("Predictions:", result["predictions"])
    #    print("Summary:", result["summary"])
    
    #print("Spark UI disponível. Pressione Ctrl+C para sair.")
    #try:
    #    while True:
    #        time.sleep(1)
    #except KeyboardInterrupt:
    #    print("Encerrando SparkContext...")
    #    spark_engine.stop_spark_session()
