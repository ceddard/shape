from .schemas import PipelineStrategy
from sklearn.pipeline import Pipeline
from pipeline.steps.sklearn import ReduceDimStrategy, QTransfStrategy, PolyFeatureStrategy, StdScalerStrategy

class SklearnPipelineStrategy(PipelineStrategy):
    def __init__(self, pipeline_spec):
        self.pipeline_spec = pipeline_spec
        self.strategies = {
            "reduce_dim": ReduceDimStrategy(),
            "qtransf": QTransfStrategy(),
            "poly_feature": PolyFeatureStrategy(),
            "stdscaler": StdScalerStrategy()
        }

    def fit_transform(self, data):
        steps = self.pipeline_spec["steps"]
        pipeline_steps = []
        
        for step_name, step_config in steps.items():
            if step_name in self.strategies:
                strategy = self.strategies[step_name]
                pipeline_steps.append(strategy.apply(step_config))
        
        pipeline = Pipeline(pipeline_steps)
        return pipeline.fit_transform(data)
