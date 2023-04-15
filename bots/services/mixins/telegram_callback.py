import datetime
import json
import re
from typing import Union

from django.conf import settings

import requests

from api import models as api_models
from api.time.time_services import TimeServices
from users import models

from ..constants import DAYS_RU
from ..telegram_dataclasses import ButtonsWithText, ResponseTelegram, ResponseDecorator
from ..decorators import response_wrapper
from .common import BaseMixin


class TelegramCallbackSettings(BaseMixin):
    _time_service = TimeServices()

    @response_wrapper
    def get_callback(self, callback_data) -> ResponseTelegram:
        data: ButtonsWithText
        data = self._handle_callback(callback_data)
        return ResponseTelegram(
            chat_id=callback_data.chat_id,
            text=data.text,
            message_id=callback_data.message_id,
            reply_markup=data.buttons,
            method="editMessageText"
        )

    @staticmethod
    def _get_button(
        text: Union[str, list], data: Union[str, list], multiple: bool = False
    ) -> list:
        if multiple:
            return [
                [{"text": text, "callback_data": call_data}]
                for text, call_data in zip(text, data)
            ]
        return [[{"text": text, "callback_data": data}]]

    def _get_quickstart_data(self):
        return ButtonsWithText(
            text=settings.MESSAGES["QUICKSTART_RU"],
            buttons=self._get_button(text=settings.MESSAGES["MENU_RU"], data="menu"),
        )

    def _get_add_data(self):
        return ButtonsWithText(
            text=settings.MESSAGES["ABOUT_ADD_TOKENS_RU"],
            buttons=self._get_button(text=settings.MESSAGES["MENU_RU"], data="menu"),
        )

    def _get_help_data(self):
        buttons = self._get_button(
            text=["Обратная связь", settings.MESSAGES["MENU_RU"]],
            data=["---", "menu"],
            multiple=True,
        )
        buttons[0]["url"] = "tg://user?id=6201041495"
        return ButtonsWithText(text=settings.MESSAGES["HELP_RU"], buttons=buttons)

    def _get_tokens_data(self):
        token = models.CustomUser.objects.filter(verified=True).first()
        inline_buttons = self._get_button(
            text=[token.username, settings.MESSAGES["MENU_RU"]],
            data=[f"about-token:{token.username}", "menu"],
            multiple=True,
        )
        return ButtonsWithText(
            text=settings.MESSAGES["ABOUT_TOKEN_RU"], buttons=inline_buttons
        )

    def _get_favorites_data(self, callback_data, call_data):
        tokens = models.TelegramUserToken.objects.filter(
            telegram_user__telegram_id=callback_data.chat_id,
        )
        inline_buttons = [
            [],  # 2 rows button
            [],
            [{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}],
        ]

        ind = -1
        for token in tokens:
            if ind == 1:
                ind = -1
            ind += 1
            inline_buttons[ind].append(
                {
                    "text": f"{token.token.username}",
                    "callback_data": f"{call_data}:{token.token.username}",  # TODO: self token
                }
            )
        return ButtonsWithText(
            text=settings.MESSAGES["MENU_FAVORITES_RU"], buttons=inline_buttons
        )

    def _get_added_or_delete_button(self, action, token, text, is_favorites=False):
        call_data = f"{action}-token:{token}"
        if is_favorites:
            call_data = f"{action}-token-self:{token.username}"
        return self._get_button(text=text, data=call_data)

    def _get_about_token_data(self, callback_data, favorites_token=False):
        about_token, token = callback_data.call_data.split(":")
        if "self" in about_token:  # TODO: self token
            favorites_token = True
        token = models.CustomUser.objects.filter(username=token).first()
        is_added_token = models.TelegramUserToken.objects.filter(
            token__username=token.username,
            telegram_user__telegram_id=callback_data.chat_id,
        )
        total_added = models.TelegramUserToken.objects.filter(
            token__username=token
        ).count()
        result = ButtonsWithText(
            text=f"Информация о токене:\n{'-' * 24}\n\nТокен - {token.username}\nГруппа - {token.group}\nДобавлено - {total_added}",
            buttons=[],
        )
        data = "menu-tokens"
        if favorites_token:
            data = "menu-favorites"
        menu = self._get_button(text=settings.MESSAGES["MENU_TOKENS_RU"], data=data)

        if is_added_token:
            button_added_or_delete = self._get_added_or_delete_button(
                "del", token.username, "Удалить токен", favorites_token
            )
        else:
            button_added_or_delete = self._get_added_or_delete_button(
                "add", token.username, "Добавить токен", favorites_token
            )

        result.buttons.append(menu)
        result.buttons.insert(0, button_added_or_delete)

        return result

    def _get_tokens_for_notification_data(self, callback_data):
        added_tokens = models.TelegramUserToken.objects.filter(
            telegram_user__telegram_id=callback_data.chat_id,
        )
        if not added_tokens:
            return ButtonsWithText(
                text=settings.MESSAGES["NOT_ADDED_TOKEN_FOR_PIN_RU"],
                buttons=self._get_button(
                    text=settings.MESSAGES["MENU_RU"], data="menu"
                ),
            )
        data = self._get_favorites_data(callback_data, call_data="pin-token")
        data.text = "Токены для уведомления:"
        return data

    def _get_time_for_notification_data(self, callback_data, h="12", m="00"):
        data = callback_data.call_data.split()[-1]
        buttons = [
            [
                {"text": "↑", "callback_data": f"plus-h {data}"},
                {"text": "↑", "callback_data": f"plus-m {data}"},
            ],  # 2 rows button
            [{"text": h, "callback_data": "---"}, {"text": m, "callback_data": "---"}],
            [
                {"text": "↓", "callback_data": f"minus-h {data}"},
                {"text": "↓", "callback_data": f"minus-m {data}"},
            ],
            [
                {
                    "text": settings.MESSAGES["MENU_TOKENS_RU"],
                    "callback_data": "menu-pin",
                },
                {"text": "Далее", "callback_data": f"pin-time:{h}-{m} {data}"},
            ],
        ]
        return ButtonsWithText(text="Выберите время:", buttons=buttons)

    def _get_minus_time(self, operator_, hour, minutes):
        if operator_.startswith("minus-m") and int(minutes) - 5 >= 0:
            minutes = str(int(minutes) - 5)
        elif operator_.startswith("minus-h") and int(hour) - 1 >= 0:
            hour = str(int(hour) - 1)
        return hour, minutes

    def _get_plus_time(self, operator_, hour, minutes):
        if operator_.startswith("plus-h") and int(hour) + 1 <= 23:
            hour = str(int(hour) + 1)
        elif operator_.startswith("plus-m") and int(minutes) + 5 <= 55:
            minutes = str(int(minutes) + 5)
        return hour, minutes

    def _change_time_for_notification_data(self, callback_data):
        operator_ = callback_data.call_data
        hour = callback_data.message["callback_query"]["message"]["reply_markup"][
            "inline_keyboard"
        ][1][0]
        minutes = callback_data.message["callback_query"]["message"]["reply_markup"][
            "inline_keyboard"
        ][1][1]
        hour, minutes = hour["text"], minutes["text"]
        if operator_.startswith("minus"):
            hour, minutes = self._get_minus_time(operator_, hour, minutes)
        elif operator_.startswith("plus"):
            hour, minutes = self._get_plus_time(operator_, hour, minutes)
        hour, minutes = hour.rjust(2, "0"), minutes.rjust(2, "0")
        return self._get_time_for_notification_data(callback_data, m=minutes, h=hour)

    def _get_action_for_notification_data(self, callback_data):
        data = callback_data
        buttons = self._get_button(
            text=[
                "Занятия на сегодня",
                "Занятия на завтра",
                settings.MESSAGES["MENU_TOKENS_RU"],
            ],
            data=[
                f"confirm-not pin-action:pty {data.call_data}",
                f"confirm-not pin-action:ptw {data.call_data}",
                f"menu-time {callback_data.call_data}",
            ],
            multiple=True,
        )

        return ButtonsWithText(text="Выберите время:", buttons=buttons)

    def _get_confirm_notification_data(self, callback_data):
        data = callback_data.call_data.split()[2:]
        hour, minute = data[0].split(":")[1].split("-")
        token = data[1].split(":")[-1]
        user = models.TelegramUser.objects.get(telegram_id=callback_data.chat_id)
        user.token = models.CustomUser.objects.get(username=token)
        user.notification_time = datetime.time(
            hour=int(hour), minute=int(minute), second=0
        )
        if "ptw" in callback_data.call_data:
            user.action = "PTW"
        else:
            user.action = "PTY"
        user.save(update_fields=["token", "action", "notification_time"])
        return ButtonsWithText(
            text=settings.MESSAGES["SUCCESS_ADDED_NOTIFICATION_RU"].format(
                token=token, date=f"{hour}:{minute}"
            ),
            buttons=self._get_button(text=settings.MESSAGES["MENU_RU"], data="menu"),
        )

    def _get_notification_data(self, callback_data):
        user = models.TelegramUser.objects.get(telegram_id=callback_data.chat_id)
        if user.action == "NONE":
            return ButtonsWithText(
                text=settings.MESSAGES["NOT_ADDED_TOKEN_FOR_UNPIN_RU"],
                buttons=self._get_button(
                    text=settings.MESSAGES["MENU_RU"], data="menu"
                ),
            )
        action = "Занятия на сегодня"
        if user.action == "PTW":
            action = "Занятия на завтра"
        return ButtonsWithText(
            text=settings.MESSAGES["ABOUT_NOTIFICATION_RU"].format(
                token=user.token.username,
                date=f"{str(user.notification_time)[:5]}\n{action}",
            ),
            buttons=self._get_button(
                text=[
                    settings.MESSAGES["CONFIRM_DELETE_NOTIFICATION_RU"],
                    settings.MESSAGES["MENU_RU"],
                ],
                data=["confirm-delete", "menu"],
                multiple=True,
            ),
        )

    def _get_confirm_delete_notification_data(self, callback_data):
        user = models.TelegramUser.objects.get(telegram_id=callback_data.chat_id)
        user.action = "NONE"
        user.token = None
        user.notification_time = None
        user.save(update_fields=["action", "token", "notification_time"])
        return ButtonsWithText(
            text=settings.MESSAGES["SUCCESS_DELETE_NOTIFICATION_RU"],
            buttons=self._get_button(text=settings.MESSAGES["MENU_RU"], data="menu"),
        )

    def _get_data_time_menu(self, callback_data):
        data = callback_data.call_data.split()
        hour, minute = data[1].split(":")[1].split("-")
        return self._get_time_for_notification_data(callback_data, h=hour, m=minute)

    def _get_data(self, callback_data):
        return self._get_quickstart_data()

    def _delete_token(self, callback_data):
        token = callback_data.call_data.split(":")[1]
        token = models.CustomUser.objects.filter(username=token).first()
        models.TelegramUserToken.objects.filter(
            token__username=token.username,
            telegram_user__telegram_id=callback_data.chat_id,
        ).delete()

    def _add_token(self, callback_data):
        token = callback_data.call_data.split(":")[1]
        token = models.CustomUser.objects.get(username=token)
        user = models.TelegramUser.objects.get(telegram_id=callback_data.chat_id)
        models.TelegramUserToken.objects.create(token=token, telegram_user=user)

    @staticmethod
    def is_callback(callback):
        try:
            _ = callback["callback_query"]["from"]["id"]
            return True
        except KeyError:
            return False

    def _handle_callback(self, callback_data):
        data = callback_data.call_data
        if data.startswith("M"):  # M - Menu
            return self._handle_callback_for_menu(callback_data)
        return self._handle_callback_for_setting(callback_data)

    def _get_data_for_buttons_of_menu(self, data, callback_data, weeks=False):
        token = callback_data.call_data.split(":")[-1]
        data += f"\n\nПоследнее обновление: {self._time_service.get_current_time(second=True)}"
        buttons = ButtonsWithText(
            text=data,
            buttons=self._get_button(
                text=settings.MESSAGES["MENU_TOKENS_RU"], data=f"MainMenu:{token}"
            ),
        )
        if not weeks:
            buttons.buttons.insert(
                0, [{"text": "Обновить 🔄", "callback_data": callback_data.call_data}]
            )

        return buttons

    def _get_number_week(self):
        return f"Номер недели - {self._time_service.get_week_number() + 1}"

    def _get_data_for_today_and_tomorrow_paris(self, callback_data, day, week, action):
        token = callback_data.call_data.split(":")[-1]
        instances = api_models.Schedule.objects.filter(
            group__username=token,
            week__name__startswith=week,
            day__name__iexact=day.name,
        ).order_by("number_pair")
        result = f"Занятия на {action} [{day.rus_name.title()}]: {week} - Неделя\n\n"
        for inst in instances:
            result += f"{inst.number_pair}) {inst.subject} {inst.teacher} {inst.type_pair} {inst.audience}\n"
        return result

    def _get_pairs(self, callback_data, is_today=True):
        day = self._time_service.get_week_day(lang="en")
        week = self._time_service.get_week_number() + 1
        action = "сегодня"
        if is_today and day.num == 6:
            return f"Сегодня выходной :) {week} - Неделя"
        if not is_today and day.num == 5:
            return f"Завтра выходной :) {week} - Неделя"
        if not is_today and day.num == 6:
            week = 1 if week + 1 == 5 else week + 1
        if not is_today:
            day = self._time_service.get_week_day(is_today=False, lang="en")
            action = "завтра"
        return self._get_data_for_today_and_tomorrow_paris(
            callback_data, day, str(week), action
        )

    def _get_teachers(self, callback_data):
        token = callback_data.call_data.split(":")[-1]
        instances = api_models.Schedule.objects.filter(
            group__username=token,
        ).distinct("teacher")
        if len(instances):
            return "\n".join([t.teacher for t in instances])
        return "Нет данных :("

    def _get_subjects(self, callback_data):
        token = callback_data.call_data.split(":")[-1]
        instances = api_models.Schedule.objects.filter(
            group__username=token,
        ).distinct("subject")
        if len(instances):
            return "\n".join([t.subject for t in instances if "(" not in t.subject])
        return "Нет данных :("

    def _get_schedule(self, callback_data):
        token = callback_data.call_data.split(":")[-1]
        week = self._time_service.get_week_number()
        week = str(1 if week + 1 > 4 else week + 1)
        instances = api_models.Schedule.objects.filter(
            group__username=token, week__name__startswith=week
        ).order_by("day_id", "number_pair")
        if len(instances):
            first_day = instances[0].day.name
            result = f"{DAYS_RU[first_day]}\n"
            for s in instances:
                if DAYS_RU[s.day.name] != first_day:
                    first_day = DAYS_RU[s.day.name]
                    result += f"\n{first_day}\n"
                result += f"{s.number_pair}) {s.subject} {s.type_pair.name} {s.teacher} {s.audience}\n"
            return result
        return "Нет данных :("

    def _handle_callback_for_setting(self, callback_data):
        """The order of conditions are important"""

        data = callback_data.call_data
        if data == "menu":
            return self.get_settings()
        elif data == "help":
            return self._get_help_data()
        elif data in ("tokens", "menu-tokens"):
            return self._get_tokens_data()
        elif data == "quickstart":
            return self._get_quickstart_data()

        elif data == "add":
            return self._get_add_data()

        elif data in ("favorites", "menu-favorites"):
            return self._get_favorites_data(callback_data, call_data="about-token-self")

        elif data in ("pin", "menu-pin"):  # Choice group
            return self._get_tokens_for_notification_data(callback_data)
        elif data.startswith("menu-time"):  # Choice group
            return self._get_data_time_menu(callback_data)

        elif data.startswith("confirm-not"):  # Confirm notification
            return self._get_confirm_notification_data(callback_data)
        elif re.search("(minus|plus)", data):  # Choice time
            return self._change_time_for_notification_data(callback_data)
        elif "pin-time" in data:  # Choice action
            return self._get_action_for_notification_data(callback_data)
        elif "pin-token" in data:  # Choice token
            return self._get_time_for_notification_data(callback_data)

        elif data == "unpin":
            return self._get_notification_data(callback_data)
        elif data == "confirm-delete":
            return self._get_confirm_delete_notification_data(callback_data)

        elif data.startswith("about-token"):
            return self._get_about_token_data(callback_data)

        elif re.match(r"(del-token|add-token)", data):
            if callback_data.call_data.startswith("del"):
                self._delete_token(callback_data)
            else:
                self._add_token(callback_data)

            if "self" in data:
                return self._get_about_token_data(callback_data, favorites_token=True)
            return self._get_about_token_data(callback_data)

    def _handle_callback_for_menu(self, callback_data):
        """The order of conditions are important"""

        data = None
        call_data = callback_data.call_data
        if call_data == "MainMenu":
            return self.get_menu(callback_data)
        if call_data.startswith("MainMenu:"):
            return self.get_menu_buttons(callback_data)
        elif call_data.startswith("MB-number-week"):
            data = self._get_number_week()
        elif call_data.startswith("MB-pairs-today"):
            data = self._get_pairs(callback_data)
        elif call_data.startswith("MB-pairs-tomorrow"):
            data = self._get_pairs(callback_data, is_today=False)
        elif call_data.startswith("MB-teachers"):
            data = self._get_teachers(callback_data)
        elif call_data.startswith("MB-subjects"):
            data = self._get_subjects(callback_data)
        elif call_data.startswith("MB-schedule"):
            data = self._get_schedule(callback_data)
        if data is not None:
            return self._get_data_for_buttons_of_menu(data, callback_data)
