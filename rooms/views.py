from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from . import models
from . import serializers


class OwnPagination(PageNumberPagination):
    page_size = 10


class RoomsView(APIView):
    def get(self, request):
        paginator = OwnPagination()
        rooms = models.Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = serializers.RoomSerializer(results, many=True).data
        return paginator.get_paginated_response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = serializers.RoomSerializer(room).data
            return Response(room_serializer, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = models.Room.objects.get(pk=pk)
            return room
        except models.Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = serializers.RoomSerializer(room).data
            return Response(serializer)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = serializers.RoomSerializer(
                room, data=request.data, partial=True
            )
            if serializer.is_valid():
                room = serializer.save()
                room_serializer = serializers.RoomSerializer(room).data
                return Response(room_serializer)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def search_room_view(request):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None)
    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None)
    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms
    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - 0.005
        filter_kwargs["lat__lte"] = float(lat) + 0.005
        filter_kwargs["lng__gte"] = float(lng) - 0.005
        filter_kwargs["lng__lte"] = float(lng) + 0.005
    paginator = OwnPagination()
    try:
        rooms = models.Room.objects.filter(**filter_kwargs)
    except ValueError:
        rooms = models.Room.objects.all()
    results = paginator.paginate_queryset(rooms, request)
    serializer = serializers.RoomSerializer(results, many=True).data
    return paginator.get_paginated_response(serializer)
