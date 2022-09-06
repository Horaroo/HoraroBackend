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

    email = models.EmailField(models.EmailField.description,
                              unique=True,
                              validators=[email_validator],
                              error_messages={
                                  "unique": "Такая почта уже используется.",
                              })

    def __str__(self):
        return self.username
