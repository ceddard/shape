import numpy as np
from loader.load import Load
from pipeline.builder import PipelineBuilder
from config import settings

class PipelineHandler:
    def __init__(self):
        self.load = Load()
        self.pipeline_context = PipelineBuilder(settings.PIPELINE_FILE_PATH, framework='sklearn') #TODO: substituir para escolher o framework do pipe no futuro
        self.pipeline = self.pipeline_context.create_pipeline_strategy()

    def process_data(self):
        data = self.load.data
        data = data[:, [0, 1, 2]]
        transformed_data = self.pipeline.fit_transform(data)
        return data, transformed_data

    def get_predictions_and_metrics(self):
        data, transformed_data = self.process_data()
        model = self.load.model

        if not len(transformed_data):
            raise RuntimeError('No data to score')
        if not hasattr(model, 'predict'):
            raise Exception('Model does not have a score function')#TODO: transformar em exceptions

        predictions = model.predict(transformed_data)
        unique, counts = np.unique(predictions, return_counts=True)
        result = dict(zip(map(str, unique), counts)) #TODO: transformar em dict comprehension

        metrics = {
            "data_shape": data.shape,
            "transformed_data_shape": transformed_data.shape,
            "unique_predictions": len(unique)
        }

        return predictions, metrics, result, data
