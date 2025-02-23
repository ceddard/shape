import pytest
from job_test_challenge import load, load_pipeline, score
import numpy as np
from sklearn.pipeline import Pipeline
from pyspark.sql import SparkSession, DataFrame as PySparkDataFrame

# revisor, calma que isso e apenas o escopo do esperado :D
spark = SparkSession.builder.appName("test").getOrCreate()

def test_load_data():
    data = load('data')
    assert data is not None
    assert isinstance(data, PySparkDataFrame)
    assert not data.rdd.isEmpty()
    assert 'vibration_x' in data.columns

def test_load_model():
    model = load('model')
    assert model is not None
    assert hasattr(model, 'predict')
    assert hasattr(model, 'score')

def test_load_pipeline():
    pipeline = load_pipeline('artifacts/pipeline.jsonc')
    assert pipeline is not None
    assert isinstance(pipeline, Pipeline)

def test_score():
    result = score()
    assert result is not None
    assert isinstance(result, np.ndarray)

def test_load_invalid_type():
    with pytest.raises(ValueError):
        load('invalid_type')
