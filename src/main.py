import datetime
import json
import os
import time
import numpy as np
import mlflow
from kafka import KafkaProducer
from pyspark.sql import SparkSession
from loader.load import Load
from pipeline.builder import PipelineContext
from logger.logger import KafkaLogger, FileLogger
from utils import save_metrics_to_json, save_to_postgres

pipeline_file_path = 'artifacts/pipeline.jsonc' #TODO: nao deixar hardcoded
data_file_path = 'data/dataset.parquet' #TODO: nao deixar hardcoded

spark = SparkSession.builder \
    .appName("Shape") \
    .config("spark.ui.port", "4040") \
    .getOrCreate()#TODO: modularizar

if not spark:
    raise RuntimeError("Falha ao iniciar o Spark Context") #TODO: modularizar Junto com o spark e criar excessao

KAFKA_TOPIC = 'pipeline_logs' #TODO: nao deixar hardcoded
KAFKA_SERVER = 'localhost:9092' #TODO: nao deixar hardcoded
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER) #TODO: modularizar para instanciar junto ao kafka

def score():
    try:
        mlflow.start_run() #TODO: modularizar para tracebality e criar excessao
        run_id = mlflow.active_run().info.run_id #TODO: modularizar para tracebality e criar excessao
        timestamp = datetime.datetime.now().isoformat() #TODO: modularizar para utils
        
        load = Load() #TODO: mover para o construtor do pacote
        m = load.model
        data = load.data
        
        pipeline_context = PipelineContext(pipeline_file_path) #TODO: refatorar junto ao pipeline
        pipe = pipeline_context.get_pipeline() #TODO: refatorar junto ao pipeline

        data = data[:, [0, 1, 2]] 
        tr_data = pipe.fit_transform(data)

        if not len(tr_data): #TODO: modularizar esse bloco para exceptions
            raise RuntimeError('No data to score')
        if not hasattr(m, 'predict'):
            raise Exception('Model does not have a score function')

        predictions = m.predict(tr_data)
        unique, counts = np.unique(predictions, return_counts=True)
        result = dict(zip(unique, counts))

        metrics = {
            "data_shape": data.shape,
            "transformed_data_shape": tr_data.shape,
            "unique_predictions": len(unique)
        }

        mlflow.log_param("data_shape", data.shape)
        mlflow.log_param("transformed_data_shape", tr_data.shape)
        mlflow.log_metric("unique_predictions", len(unique))
        
        input_example = data[:5]
        transformed_input_example = pipe.transform(input_example)
        mlflow.sklearn.log_model(m, "model", input_example=transformed_input_example) #deveria ser async

        success_message = f'{datetime.datetime.now()} - Success: Model scored successfully\n'
        producer.send(KAFKA_TOPIC, success_message.encode('utf-8'))

        metrics_file_path = os.path.join('logs', 'metrics.json')
        save_metrics_to_json(metrics, metrics_file_path)

        mlflow_info = {
            "run_id": run_id,
            "params": mlflow.active_run().data.params,
            "metrics": mlflow.active_run().data.metrics,
            "tags": mlflow.active_run().data.tags
        }
        save_to_postgres(run_id, timestamp, predictions.tolist(), result, data.tolist(), mlflow_info)

        return {
            "predictions": predictions,
            "summary": result
        }
    except Exception as e:
        print(e)
        KafkaLogger().log_failure(e)
        FileLogger().log_failure(e)
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
        spark.stop()
