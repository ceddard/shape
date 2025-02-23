import datetime
from kafka import KafkaProducer
from config import settings

class Logger:
    def log_failure(self, e):
        raise NotImplementedError()

class KafkaLogger(Logger):
    def __init__(self):
        self.KAFKA_TOPIC = settings.kafka_topic
        self.KAFKA_SERVER = settings.kafka_server
        self.producer = KafkaProducer(bootstrap_servers=self.KAFKA_SERVER)

    def log_failure(self, e):
        log_message = f'{datetime.datetime.now()} - Failure: {str(e)}\n'
        self.producer.send(self.KAFKA_TOPIC, log_message.encode('utf-8'))

class FileLogger(Logger):
    def __init__(self):
        self.LOG_DUMP_PATH = 'logs/failure.log'

    def log_failure(self, e):
        log_message = f'{datetime.datetime.now()} - Failure: {str(e)}\n'
        with open(self.LOG_DUMP_PATH, 'a') as fLog:
            fLog.write(log_message)
