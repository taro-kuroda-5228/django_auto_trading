from django.shortcuts import render
from config.forms import InputForm

# Create your views here.
def index(request):
    form = InputForm.clean_ticker
    return render(request, "auto_trading/index.html", {"form": form})
