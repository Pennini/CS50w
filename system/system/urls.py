from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.profile, name="profile"),
    path("create-view/<str:intention>", views.create_view, name="create_view"),
    path("create/<str:intention>", views.create, name="create"),
    path("calendar", views.calendar, name="calendar"),
    path("availability", views.availability, name="availability"),
]
