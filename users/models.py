from django.contrib.auth.models import AbstractUser
from .validators import UnicodeUsernameValidator, email_validator
from django.db import models


class CustomUser(AbstractUser):

    username = models.CharField(
        max_length=15,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "Логин занят.",
        })

    group = models.CharField(max_length=15)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(models.EmailField.description,
                              unique=True,
                              validators=[email_validator],
                              error_messages={
                                  "unique": "Такая почта уже используется.",
                              })

    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class TelegramUser(models.Model):
    telegram_id = models.TextField(unique=True)
    username = models.TextField()
    is_moder = models.BooleanField(default=False)

    def __str__(self):
        return self.telegram_id


class GroupUserTelegram(models.Model):
    token = models.TextField()
    group = models.TextField()
    user = models.ManyToManyField(TelegramUser)

    def __str__(self):
        return f'{self.group}'
