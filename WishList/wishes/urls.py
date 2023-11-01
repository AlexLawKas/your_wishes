from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path("wish_list/", views.WishList.as_view()),
    path("wish/", views.wishCreate),
    path("wish/<int:pk>", views.wishDetail),
    path("my_wishes/", views.myWishes),
    path("delete_wish/<int:pk>",  csrf_exempt(views.RemoveWish)),
    path("update_wish/<int:pk>", views.wishUpdate),
]
