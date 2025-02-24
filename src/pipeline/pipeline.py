import numpy as np
from loader.load import Load
from pipeline.builder import PipelineBuilder
from config import settings
from pyspark.ml.feature import VectorAssembler
from typing import Tuple, Any, Dict
from pyspark.sql import DataFrame


class PipelineHandler:
    """
    PipelineHandler class for processing data and making predictions.
    """

    def __init__(self) -> None:
        """
        Initialize the PipelineHandler with a Load instance,
        pipeline framework, and pipeline context.
        """
        self.load = Load()
        self.framework = settings.PIPELINE_FRAMEWORK
        self.pipeline_context = PipelineBuilder(
            settings.PIPELINE_FILE_PATH, framework=self.framework
        )
        self.pipeline = self.pipeline_context.create_pipeline_strategy()

    def process_data(self) -> Tuple[DataFrame, Any]:
        """
        Process the data by transforming it using a VectorAssembler.

        Returns:
            Tuple[DataFrame, Any]: A tuple containing the original data and the
            transformed data.
        """
        data = self.load.data
        assembler = VectorAssembler(
            inputCols=["vibration_x", "vibration_y", "vibration_z"],
            outputCol="features",
        )
        df = assembler.transform(data)
        df = df.repartition(10)
        transformed_data = self.pipeline.fit_transform(
            df.select("features").rdd.map(lambda row: row.features).collect()
        )
        return data, transformed_data

    def get_predictions_and_metrics(
        self,
    ) -> Tuple[np.ndarray, Dict[str, int], Dict[str, int], DataFrame]:
        """
        Get predictions and metrics for the data.

        Returns:
            Tuple[np.ndarray, Dict[str, int],
                    Dict[str, int], DataFrame]: A tuple
            containing predictions, metrics, results, and the original data.
        """
        data, transformed_data = self.process_data()
        model = self.load.model

        predictions = model.predict(transformed_data)
        unique, counts = np.unique(predictions, return_counts=True)
        result = {str(key): value for key, value in zip(unique, counts)}

        metrics = {
            "data_shape": (data.count(), len(data.columns)),
            "transformed_data_shape": transformed_data.shape,
            "unique_predictions": len(unique),
        }

        return predictions, metrics, result, data
