from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
import datetime
from rest_framework import status, serializers, generics
from rest_framework.decorators import api_view
from rest_framework import filters
from .serializers import WishSerializer
from rest_framework.response import Response
from .models import Wishes
from django_filters.rest_framework import DjangoFilterBackend

from .service import WishFilter


@api_view(['POST'])
def wishCreate(request):
    """Создать желаение"""
    wish = WishSerializer(data=request.data)
    if 'name' not in request.data or request.data['name'] == "undefined":
        return Response({'error': 'name обязательно для заполнения'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'name' in request.data and len(request.data['name']) > 50:
        return Response({'error': 'name: Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif 'description' not in request.data or request.data['description'] == "undefined":
        return Response({'error': 'description обязательно для заполнения'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'description' in request.data and len(request.data['description']) > 250:
        return Response({'error': 'description: Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'price' not in request.data or request.data['price'] == "undefined":
        return Response({'error': 'price: обязательно для заполнения'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'price' not in request.data or int(request.data['price']) < 0:
        return Response({'error': 'price: не может быть отрицательной'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'price' not in request.data or int(request.data['price']) == 0:
        return Response({'error': 'price: не может быть равна 0'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif 'reason' in request.data and len(request.data['reason']) > 50:
        return Response({'error': 'reason: Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif "deadline" in request.data and request.data['deadline'] is not None:
        date_time_str = str(request.data['deadline'])[:10]
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d').date()
        if date_time_obj < datetime.date.today():
            return Response({'error': 'deadline: не может быть в прошлом'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    wish.created_by = request.user.id

    try:
        if wish.is_valid():

            wish.save(created_by=request.user)

            return Response(wish.data, status=status.HTTP_201_CREATED)
        else:

            return Response(wish.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def wishDetail(request, pk):
    """Получить желаение по id"""
    try:
        wish = Wishes.objects.get(id=pk)
        serializer = WishSerializer(wish, many=False)
        if wish.created_by.id != request.user.id:
            return Response({'error': 'Нет прав для просмотра данного желания'},
                            status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response({'error': 'Желание не найдено'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WishList(generics.ListAPIView):
    """Получить список желаний"""
    serializer_class = WishSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = WishFilter

    def get_queryset(self):
        try:
            wishes = Wishes.objects.filter(public=True)
            if not wishes:
                return []
            return wishes
        except Exception:
            return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def myWishes(request):
    """Получить список только своих желаний"""
    try:
        wishes = Wishes.objects.filter(created_by=request.user.id)
        serializer = WishSerializer(wishes, many=True)
        return Response(serializer.data)
    except Exception:
        return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def RemoveWish(request, pk):
    """Удалить желаение"""
    try:
        wish = Wishes.objects.get(id=pk)
        if wish.created_by.id != request.user.id:
            return Response({'error': 'Можно удалить только своё желание'}, status=status.HTTP_403_FORBIDDEN)
        wish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def wishUpdate(request, pk):
    wish = Wishes.objects.get(id=pk)
    if wish.created_by.id != request.user.id:
        return Response({'error': 'Можно редактировать только своё желание'},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = WishSerializer(wish, data=request.data)
    if 'name' not in request.data or request.data['name'] == "undefined":
        return Response({'error': 'name обязательно для заполнения'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'name' in request.data and len(request.data['name']) > 50:
        return Response({'error': 'name: Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif 'description' not in request.data or request.data['description'] == "undefined":
        return Response({'error': 'description обязательно для заполнения'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'description' in request.data and len(request.data['description']) > 250:
        return Response({'error': 'description: Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'price' not in request.data or request.data['price'] == "undefined":
        return Response({'error': 'price: обязательно для заполнения'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'price' not in request.data or int(request.data['price']) < 0:
        return Response({'error': 'price: не может быть отрицательной'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif 'price' not in request.data or int(request.data['price']) == 0:
        return Response({'error': 'price: не может быть равна 0'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif 'reason' in request.data and len(request.data['reason']) > 50:
        return Response({'error': 'reason: Превышено максимальное количество символов'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif "deadline" in request.data and request.data['deadline'] is not None:
        date_time_str = str(request.data['deadline'])[:10]
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d').date()
        if date_time_obj < datetime.date.today():
            return Response({'error': 'deadline: не может быть в прошлом'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:

        if serializer.is_valid():
            serializer.save()
            wish_data = serializer.data
            return Response(wish_data, status=status.HTTP_200_OK)
        else:

            return Response(wish.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': 'Произошла системная ошибка'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
