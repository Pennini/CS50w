from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry_page, name="entry"),
    path("wiki/<str:entry>", views.entry_page, name="entry"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("random/", views.random_page, name="random"),
]
