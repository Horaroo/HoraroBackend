from django.db import models

from .telegram_user import TelegramUser
from .user import CustomUser


class TelegramUserToken(models.Model):
    token = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="tokens"
    )
