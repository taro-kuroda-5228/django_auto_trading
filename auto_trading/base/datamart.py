# datamart.py
import pandas as pd
from auto_trading.base.raw_data import RawData


class Datamart:
    """Datamart class creates pd.DataFrame composed by the value you want.
    Datamart "target" column is a objective variable. Other columns are explanatory one.
    Args:
        raw_data: stock raw data
        single_values: topical value in stock movement
        num_lag: duration you want for
        days_before: how long days you want to predict after
        ticker: ticker symbol you want information of
    Typical usage example:
        if you want to predict Microsoft corporation's 1 week after close price with using recent 10 days price movement,
        datamart_MSFT = Datamart(raw_data, 'close', 10, 7, 'MSFT').datamart
    """

    def __init__(
        self,
        raw_data: RawData,
        single_values: str,
        num_lag: int,
        days_before: int,
        ticker: str,
    ):
        self.raw_data = raw_data
        self.single_values = single_values
        self.num_lag = num_lag
        self.days_before = days_before
        self.ticker = ticker

    @property
    def _lag_data(self):
        return [
            self.raw_data[self.single_values].shift(-i) for i in range(self.num_lag + 1)
        ]

    @property
    def _lag_data_columns(self):
        return [
            f"{self.ticker}_{self.single_values}_N-{i}" for i in range(self.num_lag + 1)
        ]

    @property
    def _lag_data_index(self):
        return self.raw_data["timestamp"]

    def _target_values(self, df: pd.DataFrame, column: str):
        return [
            int(_bool)
            for _bool in df[f"{self.ticker}_{column}_N-0"]
            > df[f"{self.ticker}_{column}_N-{self.days_before}"]
        ]

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
            f"{self.ticker}_{self.single_values}_N-{i}" for i in range(self.num_lag + 1)
        ]
        return self._lag_data_frame[sorted_col_name]
