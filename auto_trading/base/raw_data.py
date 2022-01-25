# raw_data.py
import pandas as pd


class RawData:
    def __init__(self, symbol_data):
        self.symbol_data = symbol_data

    @property
    def raw_data(self):
        raw_data = pd.DataFrame(self.symbol_data)
        raw_data["datetime"] = pd.to_datetime(
            raw_data.timestamp, unit="ms"
        ).dt.strftime("%Y-%m-%d")
        raw_data.set_index("datetime", drop=True, inplace=True)
        raw_data.sort_index(ascending=False, inplace=True)
        return raw_data
