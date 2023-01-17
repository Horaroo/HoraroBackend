import json

import requests

from bots.services import messages

from .common import BaseMixin


class TelegramCommands(BaseMixin):
    def _send_command(self, message, data):
        url = (
            "https://api.telegram.org/bot5557386036:AAG6H5f_6JE5hVLYx5MH2BZLwbZ1w2lJmRw"
        )
        if message.command == "/settings":
            text = messages.TITLE_SETTINGS_RU
        else:
            text = "menu"

        r = requests.get(
            url + "/sendMessage",
            params={
                "chat_id": message.chat_id,
                "reply_markup": json.dumps(data),
                "text": text,
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
        # if command_user.command == '/settings':
        self._send_command(command_user, self.get_settings())
