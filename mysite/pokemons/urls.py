from django.urls import path

from . import views

urlpatterns = [
    path("", views.page),
    path("page=<int:num>", views.page),
    path("<str:name>", views.pokemon, name="pokemon"),
    path("search", views.search, name="search"),
]
