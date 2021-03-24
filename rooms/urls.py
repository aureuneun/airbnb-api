from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("", views.RoomsView.as_view(), name="rooms"),
    path("<int:pk>/", views.RoomView.as_view(), name="detail"),
]
