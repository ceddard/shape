from .schemas import PipelineStrategy
import sys
from pyspark.ml import Pipeline
from pipeline.steps.sparkml import (
    ReduceDimStrategy,
    QTransfStrategy,
    PolyFeatureStrategy,
    StdScalerStrategy,
)
from pyspark.sql import DataFrame


class SparkMLPipelineStrategy(PipelineStrategy):
    """
    A strategy for applying a SparkML pipeline to a DataFrame.
    """
    def __init__(self, pipeline_spec: dict):
        """
        Initialize the SparkMLPipelineStrategy with the pipeline specification.
        
        Args:
            pipeline_spec (dict): The pipeline specification.
        """
        
        self.pipeline_spec = pipeline_spec
        self.strategies = {
            "reduce_dim": ReduceDimStrategy(),
            "qtransf": QTransfStrategy(),
            "poly_feature": PolyFeatureStrategy(),
            "stdscaler": StdScalerStrategy(),
        }

    def fit_transform(self, df: DataFrame, **fit_params: dict) -> DataFrame:
        """
        Fit the pipeline to the DataFrame and transform the DataFrame.
        
        Args:
            df (DataFrame): The DataFrame to transform.
            **fit_params: Arbitrary keyword arguments containing fit parameters.
            
        Returns:
            DataFrame: The transformed DataFrame.
        """
        
        step_config = fit_params.pop("step_config", {})
        steps = self.pipeline_spec["steps"]
        pipeline_stages = []

        for step_name, step_config in steps.items():
            if step_name in self.strategies:
                strategy = self.strategies[step_name]
                stage = strategy.apply(step_config)
                pipeline_stages.append(stage)

        pipeline = Pipeline(stages=pipeline_stages)
        model = pipeline.fit(df)
        transformed_data = model.transform(df)

        expected_num_features = 136
        if (
            transformed_data.select("features").head().features.size
            != expected_num_features
        ):
            sys.stdout.write(
                f"Transformed data has {transformed_data.select('features').head().features.size} features, but the model expects {expected_num_features} features."
            )

        return transformed_data
