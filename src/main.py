import numpy as np
from loader.data_loader import load
from src.pipeline.builder import pipeline_builder
from logger import logger

pipeline_file_path = 'artifacts/pipeline.jsonc'

def main():
    """
    This function should score the model on the test data and return the score.
    """
    try:
        logger.info('Loading model...')
        m = load('model')
        logger.info('Loading data...')
        data = load('data')
        logger.info('Loading pipeline...')
        pipe = pipeline_builder(pipeline_file_path)

        data = data[:, [0, 1, 2]]  # Assuming 'vibration_x', 'vibration_y', 'vibration_z' are the first three columns
        logger.info('Transforming data...')
        tr_data = pipe.fit_transform(data)

        if not len(tr_data):
            raise RuntimeError('No data to score')
        if not hasattr(m, 'predict'):
            raise Exception('Model does not have a score function')

        logger.info('Scoring model...')
        predictions = m.predict(tr_data)
        unique, counts = np.unique(predictions, return_counts=True)
        result = dict(zip(unique, counts))

        logger.info('Scoring completed successfully.')

        return {
            "predictions": predictions,
            "summary": result
        }
    except Exception as e:
        print(e)
        return None
