import json
from .strategies.sklearn_pipeline import SklearnPipelineStrategy
from .strategies.sparkml_pipeline import SparkMLPipelineStrategy
from .strategies.schemas import PipelineStrategy


class PipelineBuilder:
    """
    PipelineBuilder class for creating a pipeline strategy based on
        a JSON pipeline specification.
    """

    def __init__(self, file_path: str, framework: str):
        """
        Initialize the PipelineBuilder with the file path to the pipeline
            specification and the framework type.

        Args:
            file_path (str): The path to the pipeline specification JSON file.
            framework (str): The type of framework to use for the pipeline.
        """
        self.file_path = file_path
        self.framework = framework

    def get_pipeline(self) -> dict:
        """
        Get the pipeline specification from the JSON file.

        Returns:
            dict: The pipeline specification.
        """
        with open(self.file_path, "r") as f:
            str_json = "\n".join(f.readlines()[3:])

        return json.loads(str_json)

    def create_pipeline_strategy(self) -> PipelineStrategy:
        """
        Create a pipeline strategy based on the framework type.

        Returns:
            PipelineStrategy: The pipeline strategy object.
        """
        pipeline_spec = self.get_pipeline()
        strategy_map = {
            "sklearn": SklearnPipelineStrategy,
            "sparkml": SparkMLPipelineStrategy,
        }
        strategy_class = strategy_map.get(self.framework)
        if not strategy_class:
            raise ValueError(f"Invalid strategy type: {self.framework}")
        return strategy_class(pipeline_spec)
