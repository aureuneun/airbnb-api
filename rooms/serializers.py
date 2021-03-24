from rest_framework import serializers
from users.serializers import UserSerializer
from . import models


class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = models.Room
        fields = [
            "bedrooms",
            "name",
            "instant_book",
            "user",
        ]
