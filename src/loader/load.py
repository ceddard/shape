import dask.dataframe as dd
import pickle
import json

class Load:
    def __init__(self, data_file_path='data/dataset.parquet', model_file_path='artifacts/pipeline.jsonc'):
        self.data_file_path = data_file_path
        self.model_file_path = model_file_path

    @property
    def data(cls):
        df = dd.read_parquet(cls.data_file_path)
        return df.compute().to_numpy()

    @property
    def model(self):
        with open(self.model_file_path, 'r') as f:
            str_json = '\n'.join(f.readlines()[3:])
        with open(json.loads(str_json)["steps"]['model'], 'rb') as f:
            return pickle.load(f)

    @property
    def pipeline(cls):
        raise NotImplementedError()