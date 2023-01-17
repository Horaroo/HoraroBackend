from users import models

from ..messages import TITLE_MENU_RU, NOT_ADDED_TOKEN_FOR_MENU_RU, TITLE_SETTINGS_RU, ABOUT_ADD_TOKENS_RU
from ..telegram_dataclasses import ButtonsWithText


class BaseMixin:
    @staticmethod
    def get_settings():
        inline_buttons = [[], [], [], []]
        ind = -1
        data = {
            "Быстрый старт": "quickstart",
            "Добавить токен": "add",
            "Избранные": "favorites",
            "Техническая поддержка": "help",
            "Токены": "tokens",
            "Добавить уведомление": "pin",
            "Удалить уведомление": "unpin",
        }
        for name, call_data in data.items():
            if ind == 3:
                ind = -1
            ind += 1
            inline_buttons[ind].append({"text": f"{name}", "callback_data": call_data})

        return ButtonsWithText(text=TITLE_SETTINGS_RU, buttons=inline_buttons)

    @staticmethod
    def get_menu(message):
        tokens = models.TelegramUserToken.objects.filter(
            telegram_user__telegram_id=message.user_id
        )
        if not tokens:
            return ButtonsWithText(
                text=NOT_ADDED_TOKEN_FOR_MENU_RU,
                buttons=[[{"text": "Добавить токен", "callback_data": "add"}]],
            )
        inline_buttons = [[], [], [], []]
        ind = -1
        for token in tokens:
            if ind == 3:
                ind = -1
            ind += 1

            inline_buttons[ind].append(
                {
                    "text": f"{token.token.username}",
                    "callback_data": f"{token.token.username}",
                }
            )

        return ButtonsWithText(text=TITLE_MENU_RU, buttons=inline_buttons)