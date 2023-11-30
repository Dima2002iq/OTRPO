from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.page, name="index"),
    path("page=<int:num>", views.page),
    path("search", views.search, name="search"),
    path("<str:name>", views.pokemon, name="pokemon"),
    path("<str:name>/fight", views.fight, name="fight"),
    path("<str:name>/fight/result", views.result, name="result"),
    path("<str:name>/save", views.save, name="save"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register", views.register, name="register"),
    path("accounts/login", views.login_view, name="login"),
    path("accounts/login/prove/", views.login_prove, name="login_prove"),
]
