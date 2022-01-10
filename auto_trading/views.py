from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "auto_trading/index.html", {})


def sample(request):
    return render(request, "static/sample.html", {})
