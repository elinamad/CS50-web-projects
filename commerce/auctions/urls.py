from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting",views.newlisting,name="newlisting"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("removeWatchList/<int:id>",views.removeWatchList,name="removeWatchList"),
    path("addWatchList/<int:id>",views.addWatchList,name="addWatchList"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("categories",views.categories,name="categories"),
    path("category/<str:category>",views.category,name="category"),
    path("addcomment/<int:id>",views.addcomment,name="addcomment"),
    path("placebid/<int:id>",views.placebid,name="placebid"),
    path('closeBids/<int:id>',views.closeBids,name="closeBids"),
    path('history',views.history,name="history"),
    path("auctions/mylistings",views.mylistings,name="mylistings"),
]
