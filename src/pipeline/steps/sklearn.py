from sklearn.preprocessing import (
    PolynomialFeatures,
    QuantileTransformer,
    StandardScaler,
)
from pipeline.steps.schemas import StepStrategy
from typing import Tuple


class ReduceDimStrategy(StepStrategy):
    """
    ReduceDimStrategy class for applying the PolynomialFeatures step.

    This class is a subclass of the StepStrategy class. It implements the apply method
    that applies the PolynomialFeatures step to the input data. The apply method takes
    a step_config dictionary as input and returns a tuple containing the step name and
    the PolynomialFeatures object.

    return: Tuple[str, PolynomialFeatures]
    """

    def apply(self, step_config: dict) -> Tuple[str, PolynomialFeatures]:
        return ("reduce_dim", PolynomialFeatures(**step_config["PolynomialFeatures"]))


class QTransfStrategy(StepStrategy):
    """
    QTransfStrategy class for applying the QuantileTransformer step.

    This class is a subclass of the StepStrategy class. It implements the apply method
    that applies the QuantileTransformer step to the input data. The apply method takes
    a step_config dictionary as input and returns a tuple containing the step name and
    the QuantileTransformer object.

    return: Tuple[str, QuantileTransformer]
    """

    def apply(self, step_config: dict) -> Tuple[str, QuantileTransformer]:
        quantile_config = step_config["QuantileTransformer"]
        n_quantiles = quantile_config.get("n_quantiles", 295)
        n_samples = step_config.get("n_samples", 5)
        n_quantiles = min(n_quantiles, n_samples)
        quantile_config["n_quantiles"] = n_quantiles
        return ("qtransf", QuantileTransformer(**quantile_config))


class PolyFeatureStrategy(StepStrategy):
    """
    PolyFeatureStrategy class for applying the PolynomialFeatures step.

    This class is a subclass of the StepStrategy class. It implements the apply method
    that applies the PolynomialFeatures step to the input data. The apply method takes
    a step_config dictionary as input and returns a tuple containing the step name and
    the PolynomialFeatures object.

    return: Tuple[str, PolynomialFeatures]
    """

    def apply(self, step_config: dict) -> Tuple[str, PolynomialFeatures]:
        return ("poly_feature", PolynomialFeatures(**step_config["PolynomialFeatures"]))


class StdScalerStrategy(StepStrategy):
    """
    StdScalerStrategy class for applying the StandardScaler step.

    This class is a subclass of the StepStrategy class. It implements the apply method
    that applies the StandardScaler step to the input data. The apply method takes
    a step_config dictionary as input and returns a tuple containing the step name and
    the StandardScaler object.

    return: Tuple[str, StandardScaler]
    """

    def apply(self, step_config: dict) -> Tuple[str, StandardScaler]:
        return ("stdscaler", StandardScaler(**step_config["StandardScaler"]))
