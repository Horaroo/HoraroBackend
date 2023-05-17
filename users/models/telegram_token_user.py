from django.db import models
from .user import CustomUser
from .telegram_user import TelegramUser


class TelegramUserToken(models.Model):
    token = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="tokens"
    )
