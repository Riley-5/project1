from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"), #create url for wiki that takes a title as input
    path("search", views.search, name="search"),
    path("create_new_page", views.create_new_page, name="create_new_page"),
    path("new_page", views.new_page, name="new_page"),
    path("random_page", views.random_page, name="random_page"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("save_edit/<str:title>", views.save_edit, name="save_edit")
]
