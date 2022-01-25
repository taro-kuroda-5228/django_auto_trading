from django.urls import reverse
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import render
from config.forms import InputForm
from auto_trading.local_settings import APIkey
import csv
import requests
import pandas as pd
import matplotlib.pyplot as plt
from auto_trading.base.name import Name
from auto_trading.base.symbol_data import SymbolData
from auto_trading.base.raw_data import RawData
from auto_trading.base.datamart import Datamart
from auto_trading.base.model import Model


# Create your views here.
def index(request):
    form = InputForm()
    return render(request, "auto_trading/index.html", {"form": form})


def inputs(request):
    ticker = request.POST.get("ticker")
    form = InputForm(request.POST)
    if form.is_valid():
        return HttpResponseRedirect(reverse("auto_trading:results"), {"ticker": ticker})
    return HttpResponse("Alphabet only!")


def get_compnay_name():
    api_key = APIkey.api_key
    CSV_URL = (
        f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}"
    )
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode("utf-8")
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        my_list = list(cr)

    data = pd.DataFrame(my_list, columns=my_list[0])
    data = data.drop(0, axis=0)
    return data


def plot(ticker: str, raw_data: RawData, num_date: int = 30):
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


def pred(model: Model):
    predicted = model.predict()[0]
    if predicted == 1:
        return "up"
    return "down"


def results(request):
    ticker = "MSFT"
    company_name = get_compnay_name().to_html()
    symbol_data = SymbolData(ticker).symbol_data
    raw_data = RawData(symbol_data).raw_data
    plot(ticker, raw_data)

    raw_data.reset_index(inplace=True)
    yeasterday_table = raw_data[:1][
        ["datetime", "low", "high", "open", "close", "volume"]
    ].set_index("datetime")
    yeasterday_table = yeasterday_table.to_html()

    datamart = Datamart(raw_data, "close", 10).datamart
    model = Model(datamart)
    up_down = pred(model)

    api_key = APIkey.api_key
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"
    r = requests.get(url)
    description = r.json()

    return render(
        request,
        "auto_trading/results.html",
        {
            "ticker": ticker,
            "company_name": company_name,
            "up_down": up_down,
            "description": description,
            "yesterday_table": yeasterday_table,
        },
    )
