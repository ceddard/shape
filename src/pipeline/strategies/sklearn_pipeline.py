from .schemas import PipelineStrategy
import sys
from sklearn.pipeline import Pipeline
from pipeline.steps.sklearn import (
    ReduceDimStrategy,
    QTransfStrategy,
    PolyFeatureStrategy,
    StdScalerStrategy,
)
from typing import Any


class SklearnPipelineStrategy(PipelineStrategy):
    """
    SklearnPipelineStrategy is a concrete implementation of the PipelineStrategy
    interface. It is responsible for applying a series of transformations to the
    input data using the sklearn library.
    """
    def __init__(self, pipeline_spec: dict):
        """
        Initialize the SklearnPipelineStrategy with the pipeline specification.
        """
        self.pipeline_spec = pipeline_spec
        self.strategies = {
            "reduce_dim": ReduceDimStrategy(),
            "qtransf": QTransfStrategy(),
            "poly_feature": PolyFeatureStrategy(),
            "stdscaler": StdScalerStrategy(),
        }

    def fit_transform(self, features: Any, **fit_params) -> Any:
        """
        Fit and transform the input features using the pipeline specification.
        
        Args:
            features (Any): The input features to transform.
            **fit_params: Arbitrary keyword arguments containing fit parameters.
            
        Returns:
            Any: The transformed features.
        """
        step_config = fit_params.pop("step_config", {})
        steps = self.pipeline_spec["steps"]
        pipeline_steps = []

        for step_name, step_config in steps.items():
            if step_name in self.strategies:
                strategy = self.strategies[step_name]
                pipeline_steps.append(strategy.apply(step_config))

        pipeline = Pipeline(pipeline_steps)
        transformed_data = pipeline.fit_transform(features)

        expected_num_features = 66
        if transformed_data.shape[1] != expected_num_features:
            sys.stdout.write(
                f"Expected {expected_num_features} features, but got {transformed_data.shape[1]}"
            )

        return transformed_data
