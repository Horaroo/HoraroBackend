from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import UnicodeUsernameValidator, UnicodeGroupValidator, email_validator
from django.db import models
import binascii
import os

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


class CustomToken(models.Model):

    key = models.CharField("Key", max_length=40, primary_key=True)

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE, verbose_name="user"
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(CustomToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return f'Token: {self.key}'
