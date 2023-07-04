
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<str:name>",views.profile, name="profile"),
    path("follow/<int:id>",views.follow, name ="follow"),
    path("unfollow/<int:id>",views.unfollow,name="unfollow"),
    path("following",views.following,name="following"),
    path("addlike/<int:id>",views.addlike,name="addlike"),
    path("removelike/<int:id>",views.removelike,name="addlike"),
    path("getlikedposts",views.getlikedposts,name="getlikedposts"),
    path("edit/<int:id>",views.edit,name="edit"),
    path("profile/edit/<int:id>",views.edit,name="edit"),
]
