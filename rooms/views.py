from rest_framework.generics import ListAPIView, RetrieveAPIView
from . import models
from . import serializers


class ListRoomsView(ListAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer


class SeeRoomView(RetrieveAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomDetailSerializer
