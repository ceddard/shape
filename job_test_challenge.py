import pandas as pd
import dask.dataframe as dd
from pyspark.sql import SparkSession
from sklearn.decomposition import PCA
from sklearn.svm import OneClassSVM, LinearSVC, NuSVR
import datetime
from sklearn.preprocessing import *
from sklearn.pipeline import Pipeline
import pickle
import numpy as np
import json
import mlflow
import mlflow.sklearn
from kafka import KafkaProducer
import os
import psycopg2
import time

pipeline_file_path = 'artifacts/pipeline.jsonc'
data_file_path = 'data/dataset.parquet'

spark = SparkSession.builder.appName("JobTestChallenge").getOrCreate()

KAFKA_TOPIC = 'pipeline_logs'
KAFKA_SERVER = 'localhost:9092'
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

# Load any asset
def load(type, **kwargs):
    if (type == 'data'):
        df = dd.read_parquet(data_file_path) # usando dask
        return df.compute().to_numpy()
    if (type == 'model'):
        with open('artifacts/pipeline.jsonc', 'r') as f:
            str_json = '\n'.join(f.readlines()[3:])
        import json
        with open(json.loads(str_json)["steps"]['model'], 'rb') as f:
            return pickle.load(f)
    if (type == 'pipeline'):
        raise NotImplementedError()
    else:
        return None

def _log_failure(e):
    LOG_DUMP_PATH = 'logs/failure.log'
    log_message = f'{datetime.datetime.now()} - Failure: {str(e)}\n'
    with open(LOG_DUMP_PATH, 'a') as fLog:
        fLog.write(log_message)
    producer.send(KAFKA_TOPIC, log_message.encode('utf-8'))

def load_pipeline(file_path: str) -> Pipeline:
    #implement a method to read the pipeline file and return a pipeline with the steps in sklearn
    with open(file_path, 'r') as f:
        # Skip the first three lines of comments
        str_json = '\n'.join(f.readlines()[3:])
    
    pipeline_spec = json.loads(str_json)
    steps = pipeline_spec["steps"]
    
    pipeline_steps = []
    
    if "reduce_dim" in steps:
        pipeline_steps.append(('reduce_dim', PolynomialFeatures(**steps["reduce_dim"]["PolynomialFeatures"])))
    
    if "qtransf" in steps:
        # TODO: Adjust n_quantiles to be less than or equal to the number of samples
        # TODO: Check if 'n_quantiles' exists in the QuantileTransformer parameters, no futuro
        if "n_quantiles" in steps["qtransf"]["QuantileTransformer"]:
            n_quantiles = min(steps["qtransf"]["QuantileTransformer"]["n_quantiles"], 295)
            pipeline_steps.append(('qtransf', QuantileTransformer(n_quantiles=n_quantiles, **steps["qtransf"]["QuantileTransformer"])))
        else:
            pipeline_steps.append(('qtransf', QuantileTransformer(**steps["qtransf"]["QuantileTransformer"])))
    
    
    if "poly_feature" in steps:
        pipeline_steps.append(('poly_feature', PolynomialFeatures(**steps["poly_feature"]["PolynomialFeatures"])))
    
    if "stdscaler" in steps:
        pipeline_steps.append(('stdscaler', StandardScaler(**steps["stdscaler"]["StandardScaler"])))
    
    return Pipeline(pipeline_steps)

def save_metrics_to_json(metrics: dict, file_path: str):
    with open(file_path, 'w') as f:
        json.dump(metrics, f)

def convert_keys(obj):
    if isinstance(obj, np.generic): # converter numpy (e.g., numpy.int64, numpy.float64) para tipos primitivos
        return obj.item()
    if isinstance(obj, (datetime.datetime, datetime.date)):# converter datas para serializados
        return obj.isoformat()
    if isinstance(obj, (set, tuple)):
        return list(obj)
    if isinstance(obj, dict):
        return {str(k): convert_keys(v) for k, v in obj.items()}# Converte recursivamente as chaves dos dicionários para str
    if isinstance(obj, list):
        return [convert_keys(item) for item in obj]
    return obj

def save_to_postgres(run_id, timestamp, predictions, summary, input_data, mlflow_info):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123", #fake senha, rs
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    
    summary_conv = convert_keys(summary)  # Converter chaves em summary e mlflow_info usando convert_keys
    mlflow_info_conv = convert_keys(mlflow_info)
    
    insert_query = """
    INSERT INTO pipeline (run_id, timestamp, predictions, summary, traceability, log_status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        [run_id],                                 # run_id: enviado como lista para atender text[]
        timestamp,                                # timestamp: string ISO
        json.dumps(predictions),                  # predictions: armazenado como texto
        json.dumps(summary_conv),                 # summary: jsonb esperado
        json.dumps(mlflow_info_conv),                   # traceability: json esperado
        [json.dumps("")]            # log_status: enviado como lista
    ))# TODO: Se logado no kafka, enviar bool aqui.
    
    conn.commit()
    cursor.close()
    conn.close()

def score():
    """
    This function should score the model on the test data and return the score.
    """
    try:
        mlflow.start_run()
        run_id = mlflow.active_run().info.run_id
        timestamp = datetime.datetime.now().isoformat()
        
        m = load('model')
        data = load('data')
        pipe = load_pipeline(pipeline_file_path)

        data = data[:, [0, 1, 2]]  # Assuming 'vibration_x', 'vibration_y', 'vibration_z' are the first three columns
        tr_data = pipe.fit_transform(data)

        if (not len(tr_data)):
            raise RuntimeError('No data to score')
        if (not hasattr(m, 'predict')):
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
        
        input_example = data[:5] # Log model with input example
        transformed_input_example = pipe.transform(input_example)
        mlflow.sklearn.log_model(m, "model", input_example=transformed_input_example)

        success_message = f'{datetime.datetime.now()} - Success: Model scored successfully\n'
        producer.send(KAFKA_TOPIC, success_message.encode('utf-8'))# Log successo para Kafka

        metrics_file_path = os.path.join('logs', 'metrics.json') #salvando para mandar para json
        save_metrics_to_json(metrics, metrics_file_path)

        mlflow_info = { #save informacoes para o postgres
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
        _log_failure(e)
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


#por que tanto codigo
#se a vida
#nao e programada
#e nem tem logica?