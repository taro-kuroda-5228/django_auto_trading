from django.urls import path
from . import views

app_name = "auto_trading"
urlpatterns = [
    path("", views.index, name="index"),
    path("inputs/", views.inputs, name="inputs"),
    path("results/", views.results, name="results"),
]
