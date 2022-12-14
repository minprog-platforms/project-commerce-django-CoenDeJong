from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("<int:id>", views.bidorclose, name="bidorclose"),
    path("<int:id>/comment", views.comment, name="comment"),
    path("<int:id>/watchlist", views.watchlist, name="watchlist"),
    path("bought", views.listing, name="bought")
]
