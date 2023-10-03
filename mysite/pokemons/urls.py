from django.urls import path

from . import views

urlpatterns = [
    path("", views.page),
    path("page=<int:num>", views.page),
    path("search", views.search, name="search"),
]
