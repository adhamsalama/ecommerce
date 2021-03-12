from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:item_id>", views.item_page, name="item_page"),
    path("listing/bid/", views.bid, name="bid"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("comment", views.comment, name="comment"),
    path("category/<str:category_name>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("watchlist/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/delete", views.delete_from_watchlist, name="delete_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist")

]
