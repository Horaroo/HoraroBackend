import json
import re

from django.conf import settings

import requests

from users import models

from ..telegram_dataclasses import ButtonsWithText
from .common import BaseMixin


class TelegramCommands(BaseMixin):
    def _send_command(self, message, data: ButtonsWithText):
        requests.get(
            settings.API_URL_TELEGRAM + "/sendMessage",
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

    def _send_start(self, message):
        try:
            models.TelegramUser.objects.get(telegram_id=message.chat_id)
        except:
            models.TelegramUser.objects.create(telegram_id=message.chat_id)
        requests.get(
            settings.API_URL_TELEGRAM + "/sendMessage",
            params={
                "chat_id": message.chat_id,
                "text": settings.MESSAGES["START_RU"],
            },
        )

    def send_command(self, command_user):
        try:
            tg_chat = models.TelegramUser.objects.get(telegram_id=command_user.chat_id)
            tg_chat.type_chat = command_user.type_chat
            tg_chat.save(update_fields=["type_chat"])
        except:
            models.TelegramUser.objects.create(
                telegram_id=command_user.chat_id, type_chat=command_user.type_chat
            )
        if "@" in command_user.command:
            command_user.command = re.search(
                r"/(settings|menu|start)(?=@(horaroBot|abulaysovBot|horaroStagingBot))",
                command_user.command,
            ).group()
        if command_user.command == "/settings":
            self._send_command(command_user, self.get_settings())
        elif command_user.command == "/menu":
            self._send_command(command_user, self.get_menu(command_user))
        elif command_user.command == "/start":
            self._send_start(command_user)
