from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import datetime
from .models import CustomUser
from .serializers import UserSerializer, RegistrationSerializer


@api_view(['GET'])
def userList(request):
    try:
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except Exception:
        return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def userProfile(request):
    try:
        user = request.user
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def userDetail(request, pk):
    try:
        user = CustomUser.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def userRegistration(request):
    user = RegistrationSerializer(data=request.data)
    if 'first_name' in request.data and request.data['first_name'] is not None and len(request.data['first_name']) > 49:
        return Response({'error': 'first_name:Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'username' in request.data and request.data['username'] is not None and len(request.data['username']) > 50:
        return Response({'error': 'username:Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'phone' in request.data and request.data['phone'] is not None and len(request.data['phone']) > 12:
        return Response({'error': 'phone:Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'last_name' in request.data and request.data['last_name'] is not None and len(request.data['last_name']) > 50:
        return Response({'error': 'last_name:Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif "date_of_birth" in request.data and request.data['date_of_birth'] is not None:
        date_time_str = request.data['date_of_birth']
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d').date()
        if date_time_obj > datetime.date.today():
            return Response({'error': 'date_of_birth: не может быть в будущем'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        if user.is_valid():
            user.save()

            user.data.pop('password')

            return Response(user.data, status=status.HTTP_201_CREATED)
        else:
            if 'username' not in user.data or user.data['username'] == "":
                return Response({'error': 'Username обязательно для заполнения'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif 'email' not in user.data or user.data['email'] == "":
                return Response({'error': 'Email обязательно для заполнения'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif 'password' not in user.data or user.data['password'] == "":
                return Response({'error': 'Password обязательно для заполнения'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif 'password2' not in user.data or user.data['password2'] == "":
                return Response({'error': 'Password2 обязательно для заполнения'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif user.data['password'] != user.data['password2']:
                return Response({'error': 'Пароли не совпадают'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def userUpdate(request):
    user = request.user
    serializer = UserSerializer(instance=user, data=request.data)

    if 'username' not in request.data or request.data['username'] == "":
        return Response({'error': 'Username обязательно для заполнения'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'email' not in request.data or request.data['email'] == "":
        return Response({'error': 'Email обязательно для заполнения'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if 'first_name' in request.data and request.data['first_name'] is not None and len(request.data['first_name']) > 49:
        return Response({'error': 'first_name:Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'username' in request.data and request.data['username'] is not None and len(request.data['username']) > 50:
        return Response({'error': 'username:Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'phone' in request.data and request.data['phone'] is not None and len(request.data['phone']) > 12:
        return Response({'error': 'phone:Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'last_name' in request.data and request.data['last_name'] is not None and len(request.data['last_name']) > 50:
        return Response({'error': 'last_name:Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif "date_of_birth" in request.data and request.data['date_of_birth'] is not None:
        date_time_str = request.data['date_of_birth']
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d').date()
        if date_time_obj > datetime.date.today():
            return Response({'error': 'date_of_birth: не может быть в будущем'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            return Response(user_data, status=status.HTTP_200_OK)
        else:

            if 'username' not in serializer.data or serializer.data['username'] == "":
                return Response({'error': 'Username обязательно для заполнения'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif 'email' not in serializer.data or serializer.data['email'] == "":
                return Response({'error': 'Email обязательно для заполнения'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif 'first_name' in serializer.data and len(serializer.data['first_name']) > 99:
                return Response({'error': 'first_name:Превышено максимальное количество символов'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif 'last_name' in serializer.data and len(serializer.data['last_name']) > 100:
                return Response({'error': 'last_name:Превышено максимальное количество символов'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
