import os
import sys
from logger import logger
from utils import get_current_timestamp, Converter
from database import postgres_saver
from database.json import save_metrics_to_json
from traceability import traceability
from engine import spark, stop_spark
from pipeline.pipeline import PipelineHandler
from traceability.traceability_recorder import TraceabilityLogger
from exceptions import PipelineFailed


def score():
    try:
        run_id = traceability.start_run()
        timestamp = get_current_timestamp()

        pipeline_handler = PipelineHandler(framewokr='sklearn')
        predictions, metrics, result, data = pipeline_handler.get_predictions_and_metrics()

        TraceabilityLogger.log_traceability_info(traceability, pipeline_handler, metrics, data)

        logger.log_success(message='Model scored successfully')

        metrics_file_path = os.path.join('logs', 'metrics.json')
        save_metrics_to_json(metrics, metrics_file_path)

        traceability_info = traceability.get_run_info()

        postgres_saver.save_to_postgres(run_id, timestamp, predictions.tolist(), result, data.collect(), traceability_info)
        logger.log_run_info(
            run_id=run_id,
            timestamp=timestamp,
            predictions=Converter.convert_keys(predictions.tolist()),
            result=Converter.convert_keys(result),
            data=Converter.convert_keys(data.collect()),
            mlflow_info=Converter.convert_keys(traceability_info)
        )

        return { "predictions": predictions,"summary": result}

    except Exception as error:
        logger.log_failure(error=error)
        raise PipelineFailed(error)
    finally:
        traceability.end_run()
        stop_spark()

if __name__ == '__main__':
    result = score()
    sys.stdout.write(str(result))
 
    #print("Spark UI disponível. Pressione Ctrl+C para sair.")
    #try:
    #    while True:
    #        time.sleep(1)
    #except KeyboardInterrupt:
    #    print("Encerrando SparkContext...")
    #   )
