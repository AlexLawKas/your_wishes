# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя"""

    class Sex(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'

    id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField("Имя", max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    last_name = models.CharField("Фамилия", max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    phone = models.CharField("Телефон", max_length=12, unique=False, null=True, blank=True)
    sex = models.CharField("Пол",
                           max_length=6,
                           choices=Sex.choices,
                           default=Sex.MALE,
                           blank=True, null=True
                           )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return 'Profile for user {}'.format(self.email)
