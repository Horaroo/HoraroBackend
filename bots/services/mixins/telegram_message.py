import json

import requests

from bots.services.messages import TITLE_SETTINGS_RU
from users import models


class TelegramMessages:
    def _send_message(self, text, message):
        url = (
            "https://api.telegram.org/bot5557386036:AAG6H5f_6JE5hVLYx5MH2BZLwbZ1w2lJmRw"
        )
        requests.get(
            url + "/sendMessage",
            params={
                "chat_id": message.chat_id,
                "text": text,
            },
        )

    @staticmethod
    def is_message(message):
        try:
            _ = message["message"]["from"]["id"]
            return not str(message["message"]["text"]).startswith("/")
        except KeyError:
            return False

    def send_message(self, message):
        token = models.CustomUser.objects.filter(username=message.text).first()
        if token:
            exists = models.TelegramUserToken.objects.filter(
                telegram_user__telegram_id=message.user_id, token_id=token
            ).exists()
            if not exists:
                user = models.TelegramUser.objects.get(telegram_id=message.user_id)
                models.TelegramUserToken.objects.create(token=token, telegram_user=user)
                self._send_message(text="Токен успешно добавлен.", message=message)
            else:
                self._send_message(text="Токен уже добавлен.", message=message)
        else:
            self._send_message(text="Токен не найден.", message=message)
