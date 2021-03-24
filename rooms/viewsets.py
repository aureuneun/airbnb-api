from rest_framework import viewsets
from . import models, serializers


class RoomViewset(viewsets.ModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
