import json

import requests

from ..telegram_dataclasses import ButtonsWithText
from .common import BaseMixin


class TelegramCommands(BaseMixin):
    def _send_command(self, message, data: ButtonsWithText):
        url = (
            "https://api.telegram.org/bot5557386036:AAG6H5f_6JE5hVLYx5MH2BZLwbZ1w2lJmRw"
        )
        requests.get(
            url + "/sendMessage",
            params={
                "chat_id": message.chat_id,
                "reply_markup": json.dumps({"inline_keyboard": data.buttons}),
                "text": data.text,
            },
        )

    @staticmethod
    def is_command(message):
        try:
            _ = message["message"]["entities"][0]["type"] == "bot_command"
            return True
        except KeyError:
            return False

    def send_command(self, command_user):
        if command_user.command == "/settings":
            self._send_command(command_user, self.get_settings())
        elif command_user.command == "/menu":
            self._send_command(command_user, self.get_menu(command_user))
