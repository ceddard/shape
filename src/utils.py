import json
import datetime
import numpy as np
import psycopg2

def save_metrics_to_json(metrics: dict, file_path: str):
    with open(file_path, 'w') as f:
        json.dump(metrics, f)

def convert_keys(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, (set, tuple)):
        return list(obj)
    if isinstance(obj, dict):
        return {str(k): convert_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_keys(item) for item in obj]
    return obj

def save_to_postgres(run_id, timestamp, predictions, summary, input_data, mlflow_info):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    
    summary_conv = convert_keys(summary)
    mlflow_info_conv = convert_keys(mlflow_info)
    
    insert_query = """
    INSERT INTO pipeline (run_id, timestamp, predictions, summary, traceability, log_status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        [run_id],
        timestamp,
        json.dumps(predictions),
        json.dumps(summary_conv),
        json.dumps(mlflow_info_conv),
        [json.dumps("")]
    ))
    
    conn.commit()
    cursor.close()
    conn.close()