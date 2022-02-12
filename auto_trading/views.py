from django.urls import reverse
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.shortcuts import render
from config.forms import InputForm
from auto_trading.local_settings_amend import API_KEY
import csv
import requests
import pandas as pd
import matplotlib.pyplot as plt
from auto_trading.base.symbol_data import SymbolData
from auto_trading.base.raw_data import RawData
from auto_trading.base.datamart import Datamart
from auto_trading.base.feature import Feature
from auto_trading.base.model import Model


# Create your views here.
def index(request):
    form = InputForm()
    return render(request, "auto_trading/index.html", {"form": form})


def inputs(request):
    """This method gets ticker symbol from index.html and sends that to views.results."""

    ticker = request.POST.get("ticker")
    form = InputForm(request.POST)
    is_valid = form.is_valid()
    if is_valid:
        return HttpResponseRedirect(reverse("auto_trading:results", args=(ticker,)))
    return HttpResponse("Alphabet only!")


def get_company_name(ticker: str) -> str:
    """This method gets real company name from ticker with using Alpha Vantage."""

    CSV_URL = (
        f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}"
    )

    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode("utf-8")
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        my_list = list(cr)

    data = pd.DataFrame(my_list, columns=my_list[0])
    data = data.drop(0, axis=0)
    data = list(data[data["symbol"] == ticker]["name"])
    return data[0]


def plot(ticker: str, raw_data: RawData, num_date: int = 30):
    """This method makes close price chart of the company.
    Args:
      ticker: ticker symbol of the company
      raw_data: Rawdata module
      num_date: How many days information you want. Default is 30
    """
    close_value_num_date = pd.Series(raw_data["close"])
    datetime_num_date = pd.Series(raw_data.index[:285])

    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(111)
    ax.plot(
        datetime_num_date,
        close_value_num_date,
        marker="o",
        markeredgecolor="k",
        color="#30A2DA",
        linestyle=":",
        linewidth=2,
    )
    ax.set_title(
        f"{ticker}'s Closing Price Last 30 Days",
        font="Times New Roman",
        size=18,
        pad=10,
    )
    ax.set_ylabel("closing price", font="Times New Roman", size=12, labelpad=10)
    ax.set_xlabel("datetime", font="Times New Roman", size=12, labelpad=10)
    fig_path = "static/images/ticker.png"
    plt.savefig(fig_path)
    # plt.show()
    plt.close()


def create_exp(num_lag, *tickers: str) -> pd.DataFrame:
    """Create explanatory variables.
    Typical usage example:
        if you want to use DIA and SPY price as explanatory variables,
        feature = create_exp('DIA', 'SPY')
    """
    features = []
    ticker_dict = {ticker: f"datamart_{ticker}" for ticker in tickers}
    for ticker in tickers:
        symbol_data = SymbolData(ticker).symbol_data
        raw_data = RawData(symbol_data).raw_data
        single_values = "close"
        days_before = 1
        ticker_dict[ticker] = Datamart(
            raw_data, single_values, num_lag, days_before, ticker
        ).datamart
        features.append(ticker_dict[ticker])

    feature = Feature(features).concat_datamarts()
    return feature


def pred(model: Model):
    """Prediction of the future price, up or down."""
    predicted = model.predict()[0]
    if predicted == 1:
        return "up"
    return "down"


def pred_future(
    raw_data: RawData, single_values: str, num_lag: int, days_before: int, ticker: str
):
    """Prediction for some duration
    Typical usage example:
        if you want to predict in a week close price, up or down,
        pred_duration(raw_data, 'close', 7, 7, ticker)
    """
    datamart = Datamart(raw_data, single_values, num_lag, days_before, ticker).datamart
    feature = create_exp(num_lag, "DIA", "SPY", "QQQ", "IWM", "^VIX", "TLT")
    model = Model(datamart, feature)
    return pred(model)


def results(request, ticker):
    company_name = get_company_name(ticker)
    symbol_data = SymbolData(ticker).symbol_data
    raw_data = RawData(symbol_data).raw_data
    plot(ticker, raw_data)

    raw_data.reset_index(inplace=True)
    yeasterday_table = raw_data[:1][
        ["datetime", "low", "high", "open", "close", "volume"]
    ].set_index("datetime")
    yeasterday_table = yeasterday_table.to_html()

    up_down_tomorrow = pred_future(raw_data, "close", 5, 1, ticker)
    up_down_1_week = pred_future(raw_data, "close", 7, 7, ticker)
    up_down_1_month = pred_future(raw_data, "close", 30, 30, ticker)

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
    r = requests.get(url)
    description = r.json()

    return render(
        request,
        "auto_trading/results.html",
        {
            "ticker": ticker,
            "company_name": company_name,
            "up_down_tomorrow": up_down_tomorrow,
            "up_down_1_week": up_down_1_week,
            "up_down_1_month": up_down_1_month,
            "description": description,
            "yesterday_table": yeasterday_table,
        },
    )
