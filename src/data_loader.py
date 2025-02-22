import pandas as pd
import pickle
import json

data_file_path = 'data/dataset.parquet'

def load(type, **kwargs):
    if type == 'data':
        df = pd.read_parquet(data_file_path)
        return df.to_numpy()
    if type == 'model':
        with open('artifacts/pipeline.jsonc', 'r') as f:
            str_json = '\n'.join(f.readlines()[3:])
        with open(json.loads(str_json)["steps"]['model'], 'rb') as f:
            return pickle.load(f)
    if type == 'pipeline':
        raise NotImplementedError()
    else:
        return None
