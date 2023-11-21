
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.compose, name="compose"),
    path("<int:user_id>", views.profile, name="profile"),
    path("/following", views.following, name="following"),
    path("posts/<int:post_id>", views.like, name="like"),
    path("follow/<int:user_id>", views.change_follow, name="follow")
]
