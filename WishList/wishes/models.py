import datetime
from django.db import models

# Create your models here.
from django.utils import timezone
from users.models import CustomUser


def current_time():
    return datetime.datetime.now()


class Wishes(models.Model):
    """Модель желания"""
    name = models.CharField("Название", max_length=200)
    description = models.CharField("Описание", max_length=1000, )
    image = models.ImageField("Изображение", upload_to='wishes/%Y/%m/%d', blank=True, null=True)
    url = models.URLField("Ссылка на продукт", blank=True, null=True)
    price = models.FloatField("Примерная цена")
    public = models.BooleanField("Флаг публичности", default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата и время создания",  default=current_time())
    updated_at = models.DateTimeField("Дата и время изменения", auto_now=True)
    reason = models.CharField("Повод", max_length=250, blank=True)
    done = models.BooleanField("Флаг выполнения", default=False)
    deadline = models.DateTimeField("Срок", blank=True, default=None, null=True)
