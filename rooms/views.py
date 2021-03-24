from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from . import serializers


@api_view(["GET"])
def list_rooms(request):
    rooms = models.Room.objects.all()
    serialized_rooms = serializers.RoomSerializer(rooms, many=True)
    return Response(serialized_rooms.data)
