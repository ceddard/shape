import pickle
import json
from typing import Any
from config import settings
from engine import spark
from pyspark.sql import DataFrame


class Load:
    def __init__(self) -> None:
        self.data_file_path: str = settings.DATA_FILE_PATH
        self.model_file_path: str = settings.PIPELINE_FILE_PATH

    @property
    def data(self) -> DataFrame:
        df = spark.read.parquet(self.data_file_path)
        return df

    @property
    def model(self) -> Any:
        with open(self.model_file_path, "r") as f:
            str_json = "\n".join(f.readlines()[3:])
        with open(json.loads(str_json)["steps"]["model"], "rb") as f:
            return pickle.load(f)

    @property
    def pipeline(self) -> Any:
        raise NotImplementedError()
