from django.urls import path

from . import views

urlpatterns = [
    path("", views.page, name="index"),
    path("page=<int:num>", views.page),
    path("<str:name>", views.pokemon, name="pokemon"),
    path("<str:name>/fight", views.fight, name="fight"),
    path("<str:name>/fight/result", views.result, name="result"),
    path("search", views.search, name="search"),
]
