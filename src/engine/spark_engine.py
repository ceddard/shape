from pyspark.sql import SparkSession
from exceptions import SparkInitializationError
from config import settings

class SparkEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SparkEngine, cls).__new__(cls)
            cls._instance._spark = None
        return cls._instance

    def __init__(self):
        self.app_name = settings.APP_NAME
        self.ui_port = settings.SPARK_UI_PORT

    @property
    def spark(self):
        if self._spark is None:
            self._spark = self.create_spark_session()
        return self._spark

    def create_spark_session(self):
        try:
            spark = SparkSession.builder \
                .appName(self.app_name) \
                .config("spark.ui.port", self.ui_port) \
                .getOrCreate()
            if not spark:
                raise SparkInitializationError("Failed to initialize Spark Session")
        except Exception as e:
            raise SparkInitializationError(f"Error initializing Spark Session: {str(e)}")
        return spark

    def stop_spark_session(self):
        if self._spark:
            self._spark.stop()
            self._spark = None