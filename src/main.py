import os
import sys
from logger.kafka_logger import Logger
from utils import convert_keys, get_current_timestamp
from database.postgres import Postgres  # Import the new class
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
postgres_saver = Postgres(dbname="postgres", user="postgres", password="123", host="localhost", port="5432")  # Create an instance of PostgresSaver

def score():
    try:
        run_id = traceability.start_run()  # TODO: modularizar para tracebality e criar excessao, ou rever implementacao futura
        timestamp = get_current_timestamp()  # Chame a função diretamente
        
        pipeline_handler = PipelineHandler()
        predictions, metrics, result, data = pipeline_handler.get_predictions_and_metrics()

        TraceabilityLogger.log_traceability_info(traceability, pipeline_handler, metrics, data)

        success_message = 'Model scored successfully'
        logger.log_success(message=success_message)

        metrics_file_path = os.path.join('logs', 'metrics.json')
        save_metrics_to_json(metrics, metrics_file_path)

        traceability_info = traceability.get_run_info()

        postgres_saver.save_to_postgres(run_id, timestamp, predictions.tolist(), result, data.tolist(), traceability_info)  # Pass traceability_info as log_info

        logger.log_run_info( #TODO: verificar conversao.
            run_id=run_id,
            timestamp=timestamp,
            predictions=convert_keys(predictions.tolist()),
            result=convert_keys(result),
            data=convert_keys(data.tolist()),
            mlflow_info=convert_keys(traceability_info)
        )

        return { # retornar uma matriz com valor da previsao para aquele campo do dataframe
            "predictions": predictions,
            "summary": result
        }
    except Exception as error:
        logger.log_failure(str(error))  # Convert error to string
        raise PipelineFailed(error)
    finally:
        traceability.end_run()

if __name__ == '__main__':
    result = score()
    sys.stdout.write(str(result))  # Convert result to string
    
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
