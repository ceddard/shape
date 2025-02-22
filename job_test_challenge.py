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

pipeline_file_path = 'artifacts/pipeline.jsonc'
data_file_path = 'data/dataset.parquet'

spark = SparkSession.builder.appName("JobTestChallenge").getOrCreate()

KAFKA_TOPIC = 'mlflow_logs'
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
        pipeline_steps.append(('qtransf', QuantileTransformer(**steps["qtransf"]["QuantileTransformer"])))
    
    if "poly_feature" in steps:
        pipeline_steps.append(('poly_feature', PolynomialFeatures(**steps["poly_feature"]["PolynomialFeatures"])))
    
    if "stdscaler" in steps:
        pipeline_steps.append(('stdscaler', StandardScaler(**steps["stdscaler"]["StandardScaler"])))
    
    return Pipeline(pipeline_steps)

def score():
    """
    This function should score the model on the test data and return the score.
    """
    try:
        mlflow.start_run()
        
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

        mlflow.log_param("data_shape", data.shape)
        mlflow.log_param("transformed_data_shape", tr_data.shape)
        mlflow.log_metric("unique_predictions", len(unique))
        
        mlflow.sklearn.log_model(m, "model")

        success_message = f'{datetime.datetime.now()} - Success: Model scored successfully\n'
        producer.send(KAFKA_TOPIC, success_message.encode('utf-8'))# Log successo para Kafka

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