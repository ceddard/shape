import pickle
import json
from typing import Any
from config import settings
from engine import spark
from pyspark.sql import DataFrame


class Load:
    """
    Load class for loading data and models.
    """
    def __init__(self) -> None:
        """
        Initialize the Load class with data and model file paths.
        """
        self.data_file_path: str = settings.DATA_FILE_PATH
        self.model_file_path: str = settings.PIPELINE_FILE_PATH

    @property
    def data(self) -> DataFrame:
        """
        Load the data from the data file path.
        
        return: DataFrame: The loaded data.
        """
        df = spark.read.parquet(self.data_file_path)
        return df

    @property
    def model(self) -> Any:
        """
        Load the model from the model file path.
        
        return: Any: The loaded model object.
        """
        with open(self.model_file_path, "r") as f:
            str_json = "\n".join(f.readlines()[3:])
        with open(json.loads(str_json)["steps"]["model"], "rb") as f:
            return pickle.load(f)

    @property
    def pipeline(self) -> Any:
        """
        Load the pipeline from the model file path.
        
        return: Any: The loaded pipeline object.
        
        Note: This method is not implemented yet.
        """
        raise NotImplementedError()
