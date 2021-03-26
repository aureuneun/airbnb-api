from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("", views.RoomsView.as_view(), name="rooms"),
    path("search/", views.search_room_view, name="search-room"),
    path("<int:pk>/", views.RoomView.as_view(), name="detail"),
]
