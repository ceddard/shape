import pytest
from unittest.mock import patch, MagicMock
from main import score
from exceptions import PipelineFailed


@patch('traceability.traceability')
@patch('utils.utils.get_current_timestamp')
@patch('pipeline.pipeline.PipelineHandler')
@patch('traceability.traceability_recorder.TraceabilityLogger')
@patch('logger.logger')
@patch('database.json.save_metrics_to_json')
@patch('database.postgres_saver')
def test_score_success(mock_postgres_saver, mock_save_metrics_to_json,
                       mock_logger, mock_traceability_logger,
                       mock_pipeline_handler, mock_get_current_timestamp,
                       mock_traceability):
    """
    Test the score function with a successful run.
    not finished yet
    """
    mock_traceability.start_run.return_value = 'test_run_id'
    mock_get_current_timestamp.return_value = '2023-01-01T00:00:00Z'
    mock_pipeline_handler_instance = MagicMock()
    mock_pipeline_handler.return_value = mock_pipeline_handler_instance
    mock_pipeline_handler_instance.get_predictions_and_metrics.return_value = (
        ['pred1', 'pred2'], {'metric1': 0.9}, 'result', 'data')
    mock_traceability.get_run_info.return_value = {'info': 'test_info'}

    result = score()

    assert result == {"predictions": ['pred1', 'pred2'], "summary": 'result'}
    mock_logger.log_success.assert_called_once_with(
        message="Model scored successfully")
    mock_postgres_saver.save_to_postgres.assert_called_once()
    mock_logger.log_run_info.assert_called_once()
    mock_traceability.end_run.assert_called_once()


@patch('traceability.traceability')
@patch('logger.logger')
def test_score_failure(mock_logger, mock_traceability):
    """
    Test the score function with a failure.

    not finised yet
    """
    mock_traceability.start_run.side_effect = Exception("Test exception")

    with pytest.raises(PipelineFailed):
        score()

    mock_logger.log_failure.assert_called_once()
    mock_traceability.end_run.assert_called_once()
