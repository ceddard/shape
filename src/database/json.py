import json

def save_metrics_to_json(metrics: dict, file_path: str):
    with open(file_path, 'w') as f:
        json.dump(metrics, f)