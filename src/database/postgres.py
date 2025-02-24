import json
import psycopg2
from utils import Converter

class Postgres:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def save_to_postgres(self, run_id, timestamp, predictions, summary, mlflow_info, log_info):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cursor = conn.cursor()
        
        summary_conv = Converter.convert_keys(summary)
        mlflow_info_conv = Converter.convert_keys(mlflow_info)
        log_info_conv = "1" if log_info else "0"

        predictions_json = json.dumps(predictions)

        insert_query = """
        INSERT INTO pipeline (run_id, timestamp, predictions, summary, traceability, log_status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            [run_id],
            timestamp,
            predictions_json,
            json.dumps(summary_conv),
            json.dumps(mlflow_info_conv),
            [log_info_conv]
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
