import re

from django.conf import settings

from users import models

from ..decorators import response_wrapper
from ..telegram_dataclasses import ResponseTelegram
from .common import BaseMixin


class TelegramCommands(BaseMixin):
    method = "sendMessage"

    @response_wrapper
    def get_command(self, command_user) -> ResponseTelegram:
        message, data = self._handle_command(command_user)
        result = ResponseTelegram(
            chat_id=message.chat_id,
            text=data.text,
            method=self.method,
            reply_markup=data.buttons,
        )

        if message.command == "/start":
            self._create_user(message)
            result.text = settings.MESSAGES["START_RU"]
            result.reply_markup = None
        return result

    @staticmethod
    def is_command(message):
        try:
            _ = message["message"]["entities"][0]["type"] == "bot_command"
            return True
        except KeyError:
            return False

    def _create_user(self, message):
        try:
            models.TelegramUser.objects.get(telegram_id=message.chat_id)
        except:
            models.TelegramUser.objects.create(
                telegram_id=message.chat_id, type_chat=message.type_chat
            )

    def _handle_command(self, command_user) -> tuple | None:
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
            return command_user, self.get_settings()
        elif command_user.command == "/menu":
            return command_user, self.get_menu(command_user)
        elif command_user.command == "/start":
            return command_user, None
