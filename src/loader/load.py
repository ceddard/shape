import pickle
import json
from config import settings
from engine import spark

class Load:
    def __init__(self):
        self.data_file_path = settings.DATA_FILE_PATH
        self.model_file_path = settings.PIPELINE_FILE_PATH

    @property
    def data(self):
        df = spark.read.parquet(self.data_file_path)
        return df

    @property
    def model(self):
        with open(self.model_file_path, 'r') as f:
            str_json = '\n'.join(f.readlines()[3:])
        with open(json.loads(str_json)["steps"]['model'], 'rb') as f:
            return pickle.load(f)

    @property
    def pipeline(self):
        raise NotImplementedError()