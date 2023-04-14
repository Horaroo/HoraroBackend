import re


from users import models

from ..decorators import ResponseWrapper
from ..telegram_dataclasses import ResponseTelegram


class TelegramMessages:
    method = "sendMessage"

    @staticmethod
    def is_message(message):
        try:
            _ = message["message"]["from"]["id"]
            return not str(message["message"]["text"]).startswith("/")
        except KeyError:
            return False

    @ResponseWrapper
    def get_message(self, message):
        text = re.match(
            r"(@abulaysovBot|@horaroStagingBot|@horaroBot) .+", message.text
        )

        if message.type_chat in ("group", "supergroup") and not text:
            return
        if text:
            message.text = message.text[message.text.find(" ") + 1 :]
        token = models.CustomUser.objects.filter(username=message.text).first()
        text = "Токен не найден."
        if token:
            exists = models.TelegramUserToken.objects.filter(
                telegram_user__telegram_id=message.chat_id, token_id=token
            ).exists()
            if not exists:
                user = models.TelegramUser.objects.get(telegram_id=message.chat_id)
                models.TelegramUserToken.objects.create(token=token, telegram_user=user)
                text = "Токен успешно добавлен."
            else:
                text = "Токен уже добавлен."
        return ResponseTelegram(text=text, chat_id=message.chat_id, method=self.method)
