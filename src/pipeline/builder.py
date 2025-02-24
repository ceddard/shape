import json

from .strategies.sklearn_pipeline import SklearnPipelineStrategy
from .strategies.sparkml_pipeline import SparkMLPipelineStrategy

class PipelineBuilder:
    def __init__(self, file_path, framework):
        self.file_path = file_path
        self.framework = framework

    def get_pipeline(self):
        with open(self.file_path, 'r') as f:
            str_json = '\n'.join(f.readlines()[3:])
        
        return json.loads(str_json) # rever esta logica

    def create_pipeline_strategy(self):
        pipeline_spec = self.get_pipeline()
        strategy_map = {
            'sklearn': SklearnPipelineStrategy,
            'sparkml': SparkMLPipelineStrategy
        }
        strategy_class = strategy_map.get(self.framework)
        if not strategy_class:
            raise ValueError(f"Invalid strategy type: {self.framework}")
        return strategy_class(pipeline_spec)
