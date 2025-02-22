import pandas as pd
from sklearn.decomposition import PCA
from sklearn.svm import OneClassSVM, LinearSVC, NuSVR
import datetime
from sklearn.preprocessing import *
from sklearn.pipeline import Pipeline
import pickle
import numpy as np
import json

pipeline_file_path = 'artifacts/pipeline.jsonc'
data_file_path = 'data/dataset.parquet'

# Load any asset
def load(type, **kwargs):
    if (type == 'data'):
        # Implement a method to read the data file and return a dataframe using numpy
        df = pd.read_parquet(data_file_path)
        return df.to_numpy()
    if (type == 'model'):
        with open('artifacts/pipeline.jsonc', 'r') as f:
            str_json = '\n'.join(f.readlines()[3:])
        import json
        with open(json.loads(str_json)["steps"]['model'], 'rb') as f:
            return pickle.load(f)
    if (type == 'pipeline'):
        raise NotImplementedError()
    else:
        return None

def _log_failure( e ) :
    LOG_DUMP_PATH = 'logs/failure.log'
    with open(LOG_DUMP_PATH, 'a') as fLog:
        fLog.write(f'{datetime.datetime.now()} - Failure: %s\n' % (str(e)))

def load_pipeline(file_path: str) -> Pipeline:
    #implement a method to read the pipeline file and return a pipeline with the steps in sklearn
    with open(file_path, 'r') as f:
        # Skip the first three lines of comments
        str_json = '\n'.join(f.readlines()[3:])
    
    pipeline_spec = json.loads(str_json)
    steps = pipeline_spec["steps"]
    
    pipeline_steps = []
    
    if "reduce_dim" in steps:
        pipeline_steps.append(('reduce_dim', PolynomialFeatures(**steps["reduce_dim"]["PolynomialFeatures"])))
    
    if "qtransf" in steps:
        pipeline_steps.append(('qtransf', QuantileTransformer(**steps["qtransf"]["QuantileTransformer"])))
    
    if "poly_feature" in steps:
        pipeline_steps.append(('poly_feature', PolynomialFeatures(**steps["poly_feature"]["PolynomialFeatures"])))
    
    if "stdscaler" in steps:
        pipeline_steps.append(('stdscaler', StandardScaler(**steps["stdscaler"]["StandardScaler"])))
    
    return Pipeline(pipeline_steps)

def score():
    """
    This function should score the model on the test data and return the score.
    """
    try:
        m = load('model')
        data = load('data')
        pipe = load_pipeline(pipeline_file_path)

        data = data[:, [0, 1, 2]]  # Assuming 'vibration_x', 'vibration_y', 'vibration_z' are the first three columns
        tr_data = pipe.fit_transform(data)

        if (not len(tr_data)):
            raise RuntimeError('No data to score')
        if (not hasattr(m, 'predict')):
            raise Exception('Model does not have a score function')

        predictions = m.predict(tr_data)
        unique, counts = np.unique(predictions, return_counts=True)
        result = dict(zip(unique, counts))

        return {
            "predictions": predictions,
            "summary": result
        }
    except Exception as e:
        print(e)
        _log_failure(e)
        return None

if __name__ == '__main__':
    result = score()
    if result:
        print("Predictions:", result["predictions"])
        print("Summary:", result["summary"])