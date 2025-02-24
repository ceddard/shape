import numpy as np
from loader.load import Load
from pipeline.builder import PipelineBuilder
from config import settings
from pyspark.ml.feature import VectorAssembler

class PipelineHandler:
    def __init__(self, framewokr):
        self.load = Load()
        self.framewokr = framewokr
        self.pipeline_context = PipelineBuilder(settings.PIPELINE_FILE_PATH, framework=self.framewokr) #TODO: substituir para escolher o framework do pipe no futuro
        self.pipeline = self.pipeline_context.create_pipeline_strategy()

    def process_data(self):
        data = self.load.data
        assembler = VectorAssembler(inputCols=['vibration_x', 'vibration_y', 'vibration_z'], outputCol='features')
        df = assembler.transform(data)
        df = df.repartition(10)
        features = df.select('features').rdd.map(lambda row: row.features).collect()
        transformed_data = self.pipeline.fit_transform(features)

        return data, transformed_data

    def get_predictions_and_metrics(self):
        data, transformed_data = self.process_data()
        model = self.load.model
        predictions = model.predict(transformed_data)
        unique, counts = np.unique(predictions, return_counts=True)
        result = {str(key): value for key, value in zip(unique, counts)}

        metrics = {
            "data_shape": (data.count(), len(data.columns)),
            "transformed_data_shape": transformed_data.shape,
            "unique_predictions": len(unique)
        }

        return predictions, metrics, result, data
