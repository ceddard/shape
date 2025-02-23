import datetime
import json
import os
import time
import numpy as np
import mlflow
from loader.load import Load
from pipeline.builder import PipelineContext
from logger.kafka_logger import KafkaFacade
from utils import save_metrics_to_json, save_to_postgres
from config import settings
from engine.spark_engine import SparkEngine

spark_engine = SparkEngine()  # TODO: mover para o construtor do pacote
spark = spark_engine.spark

logger = KafkaFacade()  # TODO: mover para o construtor do pacote

def score():
    try:
        mlflow.start_run()  # TODO: modularizar para tracebality e criar excessao
        run_id = mlflow.active_run().info.run_id  # TODO: modularizar para tracebality e criar excessao
        timestamp = datetime.datetime.now().isoformat()  # TODO: modularizar para utils
        
        load = Load()  # TODO: mover para o construtor do pacote
        m = load.model
        data = load.data
        
        pipeline_context = PipelineContext(settings.PIPELINE_FILE_PATH)  # TODO: refatorar junto ao pipeline
        pipe = pipeline_context.get_pipeline()  # TODO: refatorar junto ao pipeline

        data = data[:, [0, 1, 2]] 
        tr_data = pipe.fit_transform(data)

        if not len(tr_data):  # TODO: modularizar esse bloco para exceptions
            raise RuntimeError('No data to score')
        if not hasattr(m, 'predict'):
            raise Exception('Model does not have a score function')

        predictions = m.predict(tr_data)  # TODO: definir methodo para o predict
        unique, counts = np.unique(predictions, return_counts=True)
        result = dict(zip(unique, counts))  # TODO: refatorar este arquivo

        metrics = {  # TODO: definir funcao para metricas
            "data_shape": data.shape,
            "transformed_data_shape": tr_data.shape,
            "unique_predictions": len(unique)
        }

        mlflow.log_param("data_shape", data.shape)  # TODO: modularizar para tracebality
        mlflow.log_param("transformed_data_shape", tr_data.shape)  # TODO: modularizar para tracebality
        mlflow.log_metric("unique_predictions", len(unique))  # TODO: modularizar para tracebality
        # TODO: isso tudo deveria ser async?
        
        input_example = data[:5]  # TODO: modularizar para tracebality
        transformed_input_example = pipe.transform(input_example)  # TODO: modularizar para tracebality
        mlflow.sklearn.log_model(m, "model", input_example=transformed_input_example)  # deveria ser async??

        success_message = 'Model scored successfully'  # TODO: modularizar para logger
        logger.log_success(message=success_message)  # TODO: modularizar para logger

        metrics_file_path = os.path.join('logs', 'metrics.json')  # TODO: definir funcao para metricas
        save_metrics_to_json(metrics, metrics_file_path)  # TODO: definir funcao para metricas

        mlflow_info = {  # TODO: modularizar para tracebality
            "run_id": run_id,
            "params": mlflow.active_run().data.params,
            "metrics": mlflow.active_run().data.metrics,
            "tags": mlflow.active_run().data.tags
        }
        save_to_postgres(run_id, timestamp, predictions.tolist(), result, data.tolist(), mlflow_info)  # TODO: Definir metodo para salvar no postgres

        logger.log_run_info(run_id=run_id, timestamp=timestamp, predictions=predictions.tolist(), result=result, data=data.tolist(), mlflow_info=mlflow_info)  # Log run info

        return {  # TODO: retorno esperado
            "predictions": predictions,
            "summary": result
        }
    except Exception as error:
        print(error)
        logger.log_failure(error)
        return None
    finally:
        mlflow.end_run()

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
