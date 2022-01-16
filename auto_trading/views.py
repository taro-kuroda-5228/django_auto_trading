from django.urls import reverse
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import render
from config.forms import InputForm

# Create your views here.
def index(request):
    form = InputForm()
    return render(request, "auto_trading/index.html", {"form": form})


def inputs(request):
    ticker = request.POST.get("ticker")
    form = InputForm(request.POST)
    if form.is_valid():
        return HttpResponseRedirect(reverse("auto_trading:results"))
    return HttpResponse("Alphabet only!")


def results(request):
    return render(request, "auto_trading/results.html")
