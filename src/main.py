import datetime
import json
import os
import time
import numpy as np
import mlflow
from kafka import KafkaProducer
from pyspark.sql import SparkSession
from loader.load import LoadFactory
from pipeline.builder import PipelineContext
from logger.logger import KafkaLogger, FileLogger
from src.utils import save_metrics_to_json, save_to_postgres

pipeline_file_path = 'artifacts/pipeline.jsonc'
data_file_path = 'data/dataset.parquet'

spark = SparkSession.builder \
    .appName("Shape") \
    .config("spark.ui.port", "4040") \
    .getOrCreate()

if not spark:
    raise RuntimeError("Falha ao iniciar o Spark Context")

KAFKA_TOPIC = 'pipeline_logs'
KAFKA_SERVER = 'localhost:9092'
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

def score():
    try:
        mlflow.start_run()
        run_id = mlflow.active_run().info.run_id
        timestamp = datetime.datetime.now().isoformat()
        
        load_factory = LoadFactory(data_file_path)
        m = load_factory.load('model')
        data = load_factory.load('data')
        
        pipeline_context = PipelineContext(pipeline_file_path)
        pipe = pipeline_context.get_pipeline()

        data = data[:, [0, 1, 2]]
        tr_data = pipe.fit_transform(data)

        if not len(tr_data):
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
        mlflow.sklearn.log_model(m, "model", input_example=transformed_input_example)

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