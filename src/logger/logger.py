import datetime
from kafka import KafkaProducer
from config import settings
import json
from logger.schema import LogSchema
from utils import Converter

class Logger(LogSchema):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER)
        self.topic = settings.KAFKA_TOPIC

    def __send_message(self, message):
        self.producer.send(self.topic, message.encode('utf-8'))

    def log_failure(self, **kwargs):
        error = kwargs.get('error')
        log_message = f'{datetime.datetime.now()} - Failure: {str(error)}\n'
        self.__send_message(log_message)

    def log_run_info(self, **kwargs):
        message = {
            "run_id": kwargs.get('run_id'),
            "timestamp": kwargs.get('timestamp'),
            "predictions": kwargs.get('predictions'),
            "result": kwargs.get('result'),
            "data": kwargs.get('data'),
            "mlflow_info": kwargs.get('mlflow_info')
        }
        self.__send_message(json.dumps(Converter.convert_keys(message)))
    def log_success(self, **kwargs):
        message = kwargs.get('message')
        success_message = f'{datetime.datetime.now()} - Success: {message}\n'
        self.__send_message(success_message)