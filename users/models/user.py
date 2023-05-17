from django.contrib.auth.models import AbstractUser
from django.db import models

from ..validators import UnicodeUsernameValidator, email_validator


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=15,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "Логин занят.",
        },
    )

    group = models.CharField(max_length=15)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(
        models.EmailField.description,
        unique=True,
        validators=[email_validator],
        error_messages={
            "unique": "Такая почта уже используется.",
        },
    )

    verified = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
