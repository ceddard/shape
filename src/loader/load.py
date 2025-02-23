import dask.dataframe as dd
import pickle
import json

class LoadFactory:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path

    def load(self, type, **kwargs):
        if type == 'data':
            df = dd.read_parquet(self.data_file_path)
            return df.compute().to_numpy()
        if type == 'model':
            with open('artifacts/pipeline.jsonc', 'r') as f:
                str_json = '\n'.join(f.readlines()[3:])
            with open(json.loads(str_json)["steps"]['model'], 'rb') as f:
                return pickle.load(f)
        if type == 'pipeline':
            raise NotImplementedError()
        else:
            return None
