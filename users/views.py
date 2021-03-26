import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rooms.serializers import RoomSerializer
from rooms.models import Room
from . import serializers, models


class UsersView(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializers.UserSerializer(user).data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(serializers.UserSerializer(request.user).data)

    def put(self, request):
        serializer = serializers.UserSerializer(
            request.user, request.data, partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializers.UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RoomSerializer(request.user.favs.all(), many=True).data
        return Response(serializer)

    def put(self, request):
        pk = request.data.get("pk", None)
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if request.user.favs.filter(pk=pk):
                    request.user.favs.remove(room)
                else:
                    request.user.favs.add(room)
                return Response(RoomSerializer(request.user.favs.all(), many=True).data)
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_view(request, pk):
    try:
        user = models.User.objects.get(pk=pk)
        return Response(serializers.UserSerializer(user).data)
    except models.User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        encoded_jwt = jwt.encode(
            {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response({"token": encoded_jwt})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
