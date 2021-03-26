from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.UsersView.as_view(), name="users"),
    path("login/", views.login_view, name="login"),
    path("me/", views.MeView.as_view(), name="me"),
    path("me/favs/", views.FavsView.as_view(), name="favs"),
    path("<int:pk>/", views.user_view, name="detail"),
]
