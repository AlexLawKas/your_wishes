from rest_framework import serializers

from .models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id", "username", "first_name", "last_name", "email", "date_of_birth", "photo",
            "phone")


class RegistrationUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password")
