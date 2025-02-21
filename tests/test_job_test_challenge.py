import pytest
from job_test_challenge import load, load_pipeline, score
import numpy as np
from sklearn.pipeline import Pipeline

def test_load_data():
    # Test loading data
    data = load('data')
    assert data is not None
    assert not data.empty
    assert 'vibration_x' in data.columns

def test_load_model():
    # Test loading model
    model = load('model')
    assert model is not None
    assert hasattr(model, 'predict')
    assert hasattr(model, 'score')

def test_load_pipeline():
    # Test loading pipeline
    pipeline = load_pipeline('artifacts/pipeline.jsonc')
    assert pipeline is not None
    assert isinstance(pipeline, Pipeline)

def test_score():
    # Test scoring function
    result = score()
    assert result is not None
    assert isinstance(result, np.ndarray)
