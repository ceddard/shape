from sklearn.preprocessing import PolynomialFeatures, QuantileTransformer, StandardScaler
from pipeline.steps.schemas import StepStrategy

class ReduceDimStrategy(StepStrategy):
    def apply(self, step_config):
        return ('reduce_dim', PolynomialFeatures(**step_config["PolynomialFeatures"]))

class QTransfStrategy(StepStrategy):
    def apply(self, step_config):
        n_quantiles = step_config["QuantileTransformer"].get("n_quantiles", 1000)
        n_quantiles = min(n_quantiles, 295)
        return ('qtransf', QuantileTransformer(n_quantiles=n_quantiles, **step_config["QuantileTransformer"]))

class PolyFeatureStrategy(StepStrategy):
    def apply(self, step_config):
        return ('poly_feature', PolynomialFeatures(**step_config["PolynomialFeatures"]))

class StdScalerStrategy(StepStrategy):
    def apply(self, step_config):
        return ('stdscaler', StandardScaler(**step_config["StandardScaler"]))