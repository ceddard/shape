import datetime
import numpy as np

class Converter:
    @staticmethod
    def convert_np_generic(obj):
        return obj.item()

    @staticmethod
    def convert_datetime(obj):
        return obj.isoformat()

    @staticmethod
    def convert_set_tuple(obj):
        return list(obj)

    @staticmethod
    def convert_dict(obj):
        return {str(k): Converter.convert_keys(v) for k, v in obj.items()}

    @staticmethod
    def convert_list(obj):
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
    def convert_keys(obj):
        for key, func in Converter.dispatch_table.items():
            if isinstance(obj, key):
                return func(obj)
        return obj


def get_current_timestamp():
    return str(datetime.datetime.now().isoformat())
