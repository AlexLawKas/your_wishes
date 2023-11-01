from django.urls import path

from . import views


urlpatterns = [
    path("user_list/", views.userList),
    path("registration/", views.userRegistration),
    path("user_detail/<int:pk>", views.userDetail),
    path("user_update/", views.userUpdate),
    path("profile/", views.userProfile),
]
