import sys

from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError


class SymbolData:
    """Symbol data in json format
    This json has 6 keys, timestamp, open, low, high, close, volume.
    The max length of this data is 286.
    Args:
      ticker: Name class property's ticker
    Typical usage example:
      ticker = Name("MSFT", "US").ticker
      symbol_data = SymbolData(ticker)
    """

    period = "week"
    p_num = 365
    freq = "d"
    f_num = 1

    def __init__(self, ticker: str):
        self.ticker = ticker

    @property
    def share(self):
        return share.Share(self.ticker)

    @property
    def symbol_data(self):
        try:
            symbol_data = self.share.get_historical(
                SymbolData.period, SymbolData.p_num, SymbolData.freq, SymbolData.f_num
            )
            return symbol_data
        except YahooFinanceError as e:
            print(e.message)
            sys.exit(1)
