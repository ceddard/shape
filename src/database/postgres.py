import json
import psycopg2
from typing import List, Dict, Any
from utils import Converter
from .config import INSERT_QUERY

class Postgres:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def save_to_postgres(self, run_id: str, timestamp: str, predictions: List[Dict[str, Any]], summary: Dict[str, Any], mlflow_info: Dict[str, Any], log_info: bool) -> None:
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

        cursor.execute(INSERT_QUERY, (
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
