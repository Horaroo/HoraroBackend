from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UnicodeUsernameValidator, email_validator


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


class TelegramUser(models.Model):
    ACTION_CHOICES = (
        ("PTY", "PairsToday"),
        ("PTW", "PairsTomorrow"),
    )

    username = models.TextField()
    telegram_id = models.TextField(unique=True)
    is_moder = models.BooleanField(default=False)
    token = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Token of notifications",
    )
    action = models.CharField(max_length=255, blank=True, null=True)
    notification_time = models.IntegerField(blank=True, null=True, unique=False)
    notification_time_min = models.IntegerField(blank=True, null=True, unique=False)

    def __str__(self):
        return self.telegram_id


class TelegramUserToken(models.Model):
    token = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="tokens"
    )
