from pyspark.ml.feature import PolynomialExpansion, QuantileDiscretizer, StandardScaler
from pipeline.steps.schemas import StepStrategy
from pyspark.ml.pipeline import PipelineModel

"""
this method is not used yet, because dont have full support for the pipeline
"""

class ReduceDimStrategy(StepStrategy):
    def apply(self, step_config: dict) -> PipelineModel:
        return PolynomialExpansion(**step_config["PolynomialFeatures"])


class QTransfStrategy(StepStrategy):
    def apply(self, step_config: dict) -> PipelineModel:
        quantile_config = step_config["QuantileTransformer"]
        n_quantiles = quantile_config.get("numBuckets", 295)
        n_samples = step_config.get("n_samples", 5)
        n_quantiles = min(n_quantiles, n_samples)
        quantile_config["numBuckets"] = n_quantiles
        quantile_config.pop("output_distribution", None)
        return QuantileDiscretizer(**quantile_config)


class PolyFeatureStrategy(StepStrategy):
    def apply(self, step_config: dict) -> PipelineModel:
        return PolynomialExpansion(**step_config["PolynomialFeatures"])


class StdScalerStrategy(StepStrategy):
    def apply(self, step_config: dict) -> PipelineModel:
        scaler_config = step_config["StandardScaler"]
        if "with_mean" in scaler_config:
            scaler_config["withMean"] = scaler_config.pop("with_mean")
        if "with_std" in scaler_config:
            scaler_config["withStd"] = scaler_config.pop("with_std")
        return StandardScaler(**scaler_config)
