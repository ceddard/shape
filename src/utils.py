import datetime
import numpy as np
from typing import Any, Dict, List, Union

class Converter:
    @staticmethod
    def convert_np_generic(obj: np.generic) -> Any:
        return obj.item()

    @staticmethod
    def convert_datetime(obj: Union[datetime.datetime, datetime.date]) -> str:
        return obj.isoformat()

    @staticmethod
    def convert_set_tuple(obj: Union[set, tuple]) -> List[Any]:
        return list(obj)

    @staticmethod
    def convert_dict(obj: Dict[Any, Any]) -> Dict[str, Any]:
        return {str(k): Converter.convert_keys(v) for k, v in obj.items()}

    @staticmethod
    def convert_list(obj: List[Any]) -> List[Any]:
        return [Converter.convert_keys(item) for item in obj]

    dispatch_table = {
        np.generic: convert_np_generic,
        datetime.datetime: convert_datetime,
        datetime.date: convert_datetime,
        set: convert_set_tuple,
        tuple: convert_set_tuple,
        dict: convert_dict,
        list: convert_list
    }

    @staticmethod
    def convert_keys(obj: Any) -> Any:
        for key, func in Converter.dispatch_table.items():
            if isinstance(obj, key):
                return func(obj)
        return obj


def get_current_timestamp() -> str:
    return str(datetime.datetime.now().isoformat())
