import json

from django.conf import settings

import requests

from bots.services import mixins

from .telegram_dataclasses import *


class Telegram(
    mixins.TelegramMessages, mixins.TelegramCallbackSettings, mixins.TelegramCommands
):
    def __init__(self, token, lang="ru"):
        self.token = token
        self.lang = lang

    def _send(self, data, message):
        r = requests.get(
            settings.API_URL_TELEGRAM + "/sendMessage",
            params={
                "chat_id": message.chat_id,
                "reply_markup": json.dumps(data),
                "text": settings.MESSAGES["TITLE_SETTINGS_RU"],
            },
        )

    def handle(self, data):
        if self.is_message(data):
            message = MessageUser(data).execute()
            self.send_message(message)
        elif self.is_callback(data):
            message = CallbackUser(data).execute()
            self.send_callback(message)
        elif self.is_command(data):
            message = CommandUser(data).execute()
            self.send_command(message)

    def send_error_message(self, data):
        pass
