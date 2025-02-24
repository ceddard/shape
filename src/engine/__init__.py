from .spark_engine import SparkEngine

spark_engine = SparkEngine()
spark = spark_engine.spark
stop_spark = spark_engine.stop_spark_session