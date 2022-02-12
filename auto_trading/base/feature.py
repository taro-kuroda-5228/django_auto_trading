import pandas as pd


class Feature:
    """Feature class creates pd.DataFrame composed by explanatory variables.
    By putting datamarts of ETFs or index names listed on yahoo-finance, you can get a pd.DataFrame with explanatory variables.
    Args:
        datamarts: datamarts list you want to make explanatory variables
    Typical usage example:
        if you want to predict Microsoft corporation's price with using DIA and SPY price,
        feature = Feature([datamart_DIA, datamart_SPY]).concat_datamarts()
    """

    def __init__(self, datamarts: list):
        self._datamarts = datamarts

    def concat_datamarts(self) -> pd.DataFrame:
        self._datamarts = [
            pd.DataFrame(_datamart).drop("target", axis=1)
            for _datamart in self._datamarts
        ]
        self.df = pd.concat(
            [_datamart for _datamart in self._datamarts], axis=1
        )
        return self.df
