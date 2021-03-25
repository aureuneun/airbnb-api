from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import serializers, models


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(serializers.ReadUserSerializer(request.user).data)

    def put(self, request):
        serializer = serializers.WriteUserSerializer(
            request.user, request.data, partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializers.ReadUserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_view(request, pk):
    try:
        user = models.User.objects.get(pk=pk)
        return Response(serializers.ReadUserSerializer(user).data)
    except models.User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
