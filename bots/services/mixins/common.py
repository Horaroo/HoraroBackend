from django.conf import settings

from users import models

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
            inline_buttons[ind].append(
                {"text": f"{name}", "callback_data": call_data}
            )

        return ButtonsWithText(
            text=settings.MESSAGES["TITLE_SETTINGS_RU"],
            buttons=inline_buttons,
        )

    @staticmethod
    def get_menu(message):
        tokens = models.TelegramUserToken.objects.filter(
            telegram_user__telegram_id=message.chat_id
        )
        if not tokens:
            return ButtonsWithText(
                text=settings.MESSAGES["NOT_ADDED_TOKEN_FOR_MENU_RU"],
                buttons=[
                    [
                        {
                            "text": "Добавить токен",
                            "callback_data": "add",
                        }
                    ]
                ],
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
                    "callback_data": f"MainMenu:{token.token.username}",
                }
            )

        return ButtonsWithText(
            text=settings.MESSAGES["TITLE_MENU_RU"],
            buttons=inline_buttons,
        )

    @staticmethod
    def get_menu_buttons(message):
        inline_buttons = [[], [], [], []]
        token = message.call_data.split(":")[-1]
        ind = -1
        data = {
            "Занятия сегодня": f"MB-pairs-today:{token}",  # MenuButtons
            "Занятия завтра": f"MB-pairs-tomorrow:{token}",
            "Номер недели": f"MB-number-week:{token}",
            settings.MESSAGES["MENU_RU"]: "MainMenu",
            "Преподаватели": f"MB-teachers:{token}",
            "Расписание": f"MB-schedule:{token}",
            "Предметы": f"MB-subjects:{token}",
        }

        for name, call_data in data.items():
            if ind == 3:
                ind = -1
            ind += 1
            inline_buttons[ind].append(
                {"text": f"{name}", "callback_data": call_data}
            )

        return ButtonsWithText(
            text=settings.MESSAGES["TITLE_MENU_RU"],
            buttons=inline_buttons,
        )
