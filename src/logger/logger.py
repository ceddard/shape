import datetime
from kafka import KafkaProducer

class Logger:
    def log_failure(self, e):
        raise NotImplementedError()

class KafkaLogger(Logger):
    def __init__(self):
        self.KAFKA_TOPIC = 'pipeline_logs'
        self.KAFKA_SERVER = 'localhost:9092'
        self.producer = KafkaProducer(bootstrap_servers=self.KAFKA_SERVER)

        log_message = f'{datetime.datetime.now()} - Failure: {str(e)}\n'
        self.producer.send(self.KAFKA_TOPIC, log_message.encode('utf-8'))

class FileLogger(Logger):
    def __init__(self):
        self.LOG_DUMP_PATH = 'logs/failure.log'

    def log_failure(self, e):
        log_message = f'{datetime.datetime.now()} - Failure: {str(e)}\n'
        with open(self.LOG_DUMP_PATH, 'a') as fLog:
            fLog.write(log_message)
