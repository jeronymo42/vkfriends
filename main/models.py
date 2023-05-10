from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
# User = get_user_model()
# Модель БД для пользователя. Основные поля - id(не заведено, т.к. совпадает с PK), имя пользователя (username)

class User(AbstractUser):
    username = models.CharField(blank=False, unique=True, max_length=100, verbose_name='Логин')
    password = models.CharField(blank=False, max_length=50, verbose_name='Пароль')
    friends = models.ManyToManyField('User', blank=True)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    status = models.IntegerChoices

    class Status(models.IntegerChoices):
        NORELATONS = 0
        SEND_REQUEST = 1
        FRIENDS = 2

    status = models.IntegerField(choices=Status.choices)