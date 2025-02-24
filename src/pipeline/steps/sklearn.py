from sklearn.preprocessing import PolynomialFeatures, QuantileTransformer, StandardScaler
from pipeline.steps.schemas import StepStrategy
from typing import Tuple

class ReduceDimStrategy(StepStrategy):
    def apply(self, step_config: dict) -> Tuple[str, PolynomialFeatures]:
        return ('reduce_dim', PolynomialFeatures(**step_config["PolynomialFeatures"]))

class QTransfStrategy(StepStrategy):
    def apply(self, step_config: dict) -> Tuple[str, QuantileTransformer]:
        quantile_config = step_config["QuantileTransformer"]
        n_quantiles = quantile_config.get("n_quantiles", 295)
        n_samples = step_config.get("n_samples", 5)
        n_quantiles = min(n_quantiles, n_samples)
        quantile_config["n_quantiles"] = n_quantiles
        return ('qtransf', QuantileTransformer(**quantile_config))

class PolyFeatureStrategy(StepStrategy):
    def apply(self, step_config: dict) -> Tuple[str, PolynomialFeatures]:
        return ('poly_feature', PolynomialFeatures(**step_config["PolynomialFeatures"]))

class StdScalerStrategy(StepStrategy):
    def apply(self, step_config: dict) -> Tuple[str, StandardScaler]:
        return ('stdscaler', StandardScaler(**step_config["StandardScaler"]))