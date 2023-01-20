import json

import requests

from bots.services import mixins

from .messages import TITLE_SETTINGS_RU
from .telegram_dataclasses import *


class Telegram(
    mixins.TelegramMessages, mixins.TelegramCallbackSettings, mixins.TelegramCommands
):
    def __init__(self, token, lang="ru"):
        self.token = token
        self.lang = lang

    def _send(self, data, message):
        url = (
            "https://api.telegram.org/bot5557386036:AAG6H5f_6JE5hVLYx5MH2BZLwbZ1w2lJmRw"
        )
        r = requests.get(
            url + "/sendMessage",
            params={
                "chat_id": message.chat_id,
                "reply_markup": json.dumps(data),
                "text": TITLE_SETTINGS_RU,
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
