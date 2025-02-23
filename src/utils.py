import datetime
import numpy as np

def convert_keys(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, (set, tuple)):
        return list(obj)
    if isinstance(obj, dict):
        return {str(k): convert_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_keys(item) for item in obj]
    return obj


def get_current_timestamp():
    return str(datetime.datetime.now().isoformat())
