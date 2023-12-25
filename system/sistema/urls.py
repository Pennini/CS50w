from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("search", views.search, name="search"),
    path("display/<str:type_info>/<int:id>", views.display, name="display"),
    path("profile", views.profile, name="profile"),
    path("create-view/<str:intention>", views.create_view, name="create_view"),
    path("create/<str:intention>", views.create, name="create"),
    path("bio", views.bio, name="bio"),
    path("availability", views.availability, name="availability"),
    path("calendar", views.calendar, name="calendar"),
    path("meeting", views.meeting, name="meeting"),
    path("meeting/members", views.meeting_members, name="meeting_members"),
    path("meeting/finish", views.meeting_finish, name="meeting_finish"),
]