import datetime
from kafka import KafkaProducer
from config import settings
import json
from logger.schema import LogSchema
from utils import Converter
from typing import Any


class Logger(LogSchema):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER)
        self.topic = settings.KAFKA_TOPIC

    def __send_message(self, message: str) -> None:
        self.producer.send(self.topic, message.encode("utf-8"))

    def log_failure(self, error: Exception) -> None:
        log_message = f"{datetime.datetime.now()} - Failure: {str(error)}\n"  # TODO: implementar funcao de hora aqui
        self.__send_message(log_message)

    def log_run_info(
        self,
        run_id: str,
        timestamp: str,
        predictions: Any,
        result: Any,
        data: Any,
        mlflow_info: Any,
    ) -> None:
        message = {
            "run_id": run_id,
            "timestamp": timestamp,
            "predictions": predictions,
            "result": result,
            "data": data,
            "mlflow_info": mlflow_info,
        }
        self.__send_message(json.dumps(Converter.convert_keys(message)))

    def log_success(self, message: str) -> None:
        success_message = f"{datetime.datetime.now()} - Success: {message}\n"
        self.__send_message(success_message)
