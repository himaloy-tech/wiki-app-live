from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.details, name="wiki"),
    path("search", views.search, name="search"),
    path('create', views.create, name="create"),
    path('edit/<str:title>', views.edit, name="edit-page"),
    path('save', views.save_edit, name="save-edit"),
    path('random', views.random, name="random")
]