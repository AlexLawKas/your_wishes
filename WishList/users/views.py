from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import serializers
from .models import CustomUser
from .serializers import UserListSerializer, RegistrationUserSerializer


class UserListView(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserListSerializer(users, many=True)

        return Response(serializer.data)


class RegistrationUserView(APIView):
    """Регистрация пользователя"""

    def post(self, request):
        user = RegistrationUserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

