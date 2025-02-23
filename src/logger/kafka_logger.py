import datetime
from kafka import KafkaProducer
from config import settings
import json
from logger.base_logger import Logger

class KafkaFacade(Logger):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER)
        self.topic = settings.KAFKA_TOPIC

    def __send_message(self, message):
        self.producer.send(self.topic, message.encode('utf-8'))

    def log_failure(self, e):
        log_message = f'{datetime.datetime.now()} - Failure: {str(e)}\n'
        self.__send_message(log_message)

    def log_run_info(self, run_id, timestamp, predictions, result, data, mlflow_info):
        message = {
            "run_id": run_id,
            "timestamp": timestamp,
            "predictions": predictions,
            "result": result,
            "data": data,
            "mlflow_info": mlflow_info
        }
        self.__send_message(json.dumps(message))

    def log_success(self, message):
        success_message = f'{datetime.datetime.now()} - Success: {message}\n'
        self.__send_message(success_message)
