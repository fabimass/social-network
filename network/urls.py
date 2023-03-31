
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_post, name="newpost"),
    path("likes/<int:postid>", views.likes),
    path("user/<str:username>", views.user_page, name="userpage"),
    path("user/<str:username>/follow", views.follow),
    path("following", views.following, name="following")
]
