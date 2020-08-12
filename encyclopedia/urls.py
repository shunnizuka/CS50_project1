from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entryPage, name="title"),
    path("search", views.search, name="search"),
    path("createEntry", views.createEntry, name="createEntry"),
    path("editEntry/<str:title>", views.editEntry, name="editEntry")
]
