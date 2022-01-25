# datamart.py
import pandas as pd


class Datamart:
    def __init__(self, raw_data, single_values: str, num_lag: int):
        self.raw_data = raw_data
        self.single_values = single_values
        self.num_lag = num_lag

    @property
    def _lag_data(self):
        return [
            self.raw_data[self.single_values].shift(-i) for i in range(self.num_lag + 1)
        ]

    @property
    def _lag_data_columns(self):
        return [f"{self.single_values}_N-{i}" for i in range(self.num_lag + 1)]

    @property
    def _lag_data_index(self):
        return self.raw_data["timestamp"]

    def _target_values(self, df: pd.DataFrame, column: str):
        return [int(_bool) for _bool in df[f"{column}_N-0"] > df[f"{column}_N-1"]]

    @property
    def _lag_data_frame(self):
        _lag_data_frame = pd.concat(
            self._lag_data,
            axis=1,
        )
        _lag_data_frame.columns = self._lag_data_columns
        _lag_data_frame.index = self._lag_data_index
        _lag_data_frame.dropna(inplace=True)
        _lag_data_frame["target"] = self._target_values(
            _lag_data_frame, self.single_values
        )
        return _lag_data_frame

    @property
    def datamart(self):
        sorted_col_name = ["target"] + [
            f"{self.single_values}_N-{i}" for i in range(self.num_lag + 1)
        ]
        return self._lag_data_frame[sorted_col_name]
