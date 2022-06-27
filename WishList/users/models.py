

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField("Имя", max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    last_name = models.CharField("Фамилия", max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    phone = models.CharField("Телефон", max_length=12, unique=False, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return 'Profile for user {}'.format(self.email)
