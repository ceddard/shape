import datetime
from kafka import KafkaProducer
from config import settings
import json
from logger.schema import LogSchema
from utils import Converter


class Logger(LogSchema):
    """
    Logger class for sending log messages to a Kafka topic.
    """

    def __init__(self) -> None:
        """
        Initialize the Logger with Kafka producer and topic settings.
        """
        self.producer = KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER)
        self.topic = settings.KAFKA_TOPIC

    def __send_message(self, message) -> None:
        """
        Send a message to the Kafka topic.

        Args:
            message (str): The message to send.
        """
        self.producer.send(self.topic, message.encode("utf-8"))

    def log_failure(self, **kwargs) -> None:
        """
        Log a failure message.

        Args:
            **kwargs: Arbitrary keyword arguments containing error information.
        """
        error = kwargs.get("error")
        log_message = f"{datetime.datetime.now()} - Failure: {str(error)}\n"
        self.__send_message(log_message)

    def log_run_info(self, **kwargs) -> None:
        """
        Log run information.

        Args:
            **kwargs: Arbitrary keyword arguments containing run information.
        """
        message = {
            "run_id": kwargs.get("run_id"),
            "timestamp": kwargs.get("timestamp"),
            "predictions": kwargs.get("predictions"),
            "result": kwargs.get("result"),
            "data": kwargs.get("data"),
            "mlflow_info": kwargs.get("mlflow_info"),
        }
        self.__send_message(json.dumps(Converter.convert_keys(message)))

    def log_success(self, **kwargs) -> None:
        """
        Log a success message.

        Args:
            **kwargs: Arbitrary keyword arguments containing
                success information.
        """
        message = kwargs.get("message")
        success_message = f"{datetime.datetime.now()} - Success: {message}\n"
        self.__send_message(success_message)
