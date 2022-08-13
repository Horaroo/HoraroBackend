from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import UnicodeUsernameValidator, UnicodeGroupValidator, email_validator


class CustomUser(AbstractUser):

    username = models.CharField(
        max_length=15,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "Логин занят.",
        })

    group = models.CharField(max_length=10,
                             unique=True,
                             validators=[UnicodeGroupValidator()],
                             error_messages={
                                 "unique": "Группа с таким именем уже зарегистрирована."
                             })

    email = models.EmailField(models.EmailField.description,
                              unique=True,
                              validators=[email_validator],
                              error_messages={
                                  "unique": "Такая почта уже используется.",
                              })

    def __str__(self):
        return self.username
