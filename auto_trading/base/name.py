class Name:
    """Stock name class
    If you wanna get Japanese stock name instance, you should input 4 digits security code.
    If you wanna get American stock name instance, you should input ticker symbol.
    Args:
      name: company's ticker
      nation: listed country
    """

    def __init__(self, company_ticker: str, nation: str):
        self.company_ticker = company_ticker
        self.nation = nation

    @property
    def ticker(self):
        """Ticker inputted yahoo_finance_api2."""

        if self.nation == "JP":
            self.company_ticker += ".T"

        return self.company_ticker
