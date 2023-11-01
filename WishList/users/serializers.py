import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    username = serializers.CharField(validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                                                 message=f'Пользователь с таким никнеймом уже '
                                                                         f'существует')])
    email = serializers.CharField(validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                                              message=f'Пользователь с таким email уже '
                                                                      f'существует')])

    class Meta:
        model = CustomUser
        fields = (
            'id', 'first_name', 'last_name', 'email', 'date_of_birth', 'photo', 'phone', 'sex', 'password', 'password2',
            'username')

    def create(self, validated_data):
        password = validated_data["password"]
        password2 = validated_data["password2"]
        email = validated_data["email"]
        if password != password2:
            return {"password": "Пароли не совпадают"}

        print(validated_data)
        if "first_name" not in validated_data:
            validated_data["first_name"] = None
        first_name = validated_data["first_name"]
        if 'username' not in validated_data or validated_data['username'] == "":
            return serializers.ValidationError({"username": "Обязательоне поле"})

        username = validated_data["username"]
        if "last_name" not in validated_data:
            validated_data["last_name"] = None
        last_name = validated_data["last_name"]
        if "date_of_birth" not in validated_data:
            validated_data["date_of_birth"] = None
        date_of_birth = validated_data["date_of_birth"]

        if "phone" not in validated_data:
            validated_data["phone"] = None
        phone = validated_data["phone"]
        if "sex" not in validated_data:
            validated_data["sex"] = 'Male'
        sex = validated_data["sex"]
        user = CustomUser(password=password, email=email, first_name=first_name,
                          last_name=last_name,
                          date_of_birth=date_of_birth,
                          phone=phone, sex=sex, username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                                                 message=f'Пользователь с таким никнеймом уже '
                                                                         f'существует')])
    email = serializers.CharField(validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                                              message=f'Пользователь с таким email уже '
                                                                      f'существует')])

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'photo', 'email', 'phone', 'sex', 'username')
        extra_kwargs = {'password': {'required': False}}

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        date_of_birth = validated_data["date_of_birth"]
        phone = validated_data["phone"]
        sex = validated_data["sex"]
        user = CustomUser(username=username, first_name=first_name,
                          last_name=last_name, email=email,
                          date_of_birth=date_of_birth,
                          phone=phone, sex=sex)

        user.save()
        return user
