import json


def save_metrics_to_json(metrics: dict, file_path: str):
    """
    Save a dictionary of metrics to a JSON file.
    Args:
        metrics (dict): training metrics to save.
        file_path (str): path to save the metrics.
    """
    with open(file_path, "w") as f:
        json.dump(metrics, f)
