from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_auction, name="create"),
    path("<int:auction>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:category>", views.category_list, name="category_list"),
    path("watchlist/<int:auction_id>", views.change_watchlist, name="change_watchlist"),
    path("close/<int:auction_id>", views.close, name="close"),
    path("comment/<int:auction_id>", views.comment, name="comment"),
]
