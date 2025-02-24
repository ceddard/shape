from pyspark.sql import SparkSession
from exceptions import SparkInitializationError
from config import settings


class SparkEngine:
    """
    Singleton class for managing a Spark Session.
    """
    
    _instance = None

    def __new__(cls) -> "SparkEngine":
        """
        Create a new instance of the SparkEngine class if one does not already exist.

        Returns:
            SparkEngine: Singleton instance of the SparkEngine class.
        """
        if cls._instance is None:
            cls._instance = super(SparkEngine, cls).__new__(cls)
            cls._instance._spark = None
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the SparkEngine with Spark application settings.
        """
        self.app_name: str = settings.APP_NAME
        self.ui_port: int = settings.SPARK_UI_PORT

    @property
    def spark(self) -> SparkSession:
        """
        Get the Spark Session instance.
        
        Returns:
            SparkSession: The Spark Session instance.
        """
        if self._spark is None:
            self._spark = self.create_spark_session()
        return self._spark

    def create_spark_session(self) -> SparkSession:
        """
        Create a new Spark Session instance.
        
        Returns:
            SparkSession: The new Spark Session instance.
        
        Raises:
            SparkInitializationError: If an error occurs while initializing the Spark Session.
        """
        try:
            spark = (
                SparkSession.builder.appName(self.app_name)
                .config("spark.ui.port", self.ui_port)
                .getOrCreate()
            )
            if not spark:
                raise SparkInitializationError("Failed to initialize Spark Session")
        except Exception as e:
            raise SparkInitializationError(
                f"Error initializing Spark Session: {str(e)}"
            )
        return spark

    def stop_spark_session(self) -> None:
        """
        Stop the Spark Session instance.
        """
        if self._spark:
            self._spark.stop()
            self._spark = None
