import datetime
import json
import re

from django.conf import settings

import requests

from api import models as api_models
from api.time.time_services import TimeServices
from users import models

from ..telegram_dataclasses import ButtonsWithText
from .common import BaseMixin


class TelegramCallbackSettings(BaseMixin):
    _time_service = TimeServices()

    def _get_quickstart_data(self):
        return ButtonsWithText(
            text=settings.MESSAGES["QUICKSTART_RU"],
            buttons=[[{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}]],
        )

    def _get_add_data(self):
        return ButtonsWithText(
            text=settings.MESSAGES["ABOUT_ADD_TOKENS_RU"],
            buttons=[[{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}]],
        )

    def _get_help_data(self):
        return ButtonsWithText(
            text=settings.MESSAGES["HELP_RU"],
            buttons=[
                [
                    {
                        "text": "Обратная связь",
                        "url": "tg://user?id=5710085464",
                        "callback_data": "---",
                    }
                ],
                [{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}],
            ],
        )

    def _get_tokens_data(self):
        token = models.CustomUser.objects.filter(verified=True).first()
        inline_buttons = [
            [
                {
                    "text": f"{token.username}",
                    "callback_data": f"about-token:{token.username}",
                }
            ],
            [{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}],
        ]
        return ButtonsWithText(
            text=settings.MESSAGES["ABOUT_TOKEN_RU"], buttons=inline_buttons
        )

    def _get_favorites_data(self, callback_data, call_data):
        tokens = models.TelegramUserToken.objects.filter(
            telegram_user__telegram_id=callback_data.user_id,
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

    def _get_about_token_data(self, callback_data, favorites_token=False):
        about_token, token = callback_data.call_data.split(":")
        if "self" in about_token:  # TODO: self token
            favorites_token = True
        token = models.CustomUser.objects.filter(username=token).first()
        is_added_token = models.TelegramUserToken.objects.filter(
            token__username=token.username,
            telegram_user__telegram_id=callback_data.user_id,
        )
        total_added = models.TelegramUserToken.objects.filter(
            token__username=token
        ).count()
        result = ButtonsWithText(
            text=f"Информация о токене:\n{'-' * 24}\n\nТокен - {token.username}\nГруппа - {token.group}\nДобавлено - {total_added}",
            buttons=[],
        )
        if favorites_token:
            menu = [
                {
                    "text": settings.MESSAGES["MENU_TOKENS_RU"],
                    "callback_data": "menu-favorites",
                }
            ]
        else:
            menu = [
                {
                    "text": settings.MESSAGES["MENU_TOKENS_RU"],
                    "callback_data": "menu-tokens",
                }
            ]

        if is_added_token:
            if favorites_token:
                call_data = f"del-token-self:{token.username}"
            else:
                call_data = f"del-token:{token.username}"
            button_added_or_delete = [
                {
                    "text": "Удалить токен",
                    "callback_data": call_data,
                }
            ]
        else:
            if favorites_token:
                call_data = f"add-token-self:{token.username}"
            else:
                call_data = f"add-token:{token.username}"
            button_added_or_delete = [
                {
                    "text": "Добавить токен",
                    "callback_data": call_data,
                }
            ]

        result.buttons.append(menu)
        result.buttons.insert(0, button_added_or_delete)

        return result

    def _get_tokens_for_notification_data(self, callback_data):
        added_tokens = models.TelegramUserToken.objects.filter(
            telegram_user__telegram_id=callback_data.user_id,
        )
        if not added_tokens:
            return ButtonsWithText(
                text=settings.MESSAGES["NOT_ADDED_TOKEN_FOR_PIN_RU"],
                buttons=[
                    [{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}]
                ],
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
        buttons = [
            [
                {
                    "text": "Занятия на сегодня",
                    "callback_data": f"confirm-not pin-action:pty {data.call_data}",
                }
            ],  # 2 rows button
            [
                {
                    "text": "Занятия на завтра",
                    "callback_data": f"confirm-not pin-action:ptw {data.call_data}",
                }
            ],
            [
                {
                    "text": settings.MESSAGES["MENU_TOKENS_RU"],
                    "callback_data": f"menu-time {callback_data.call_data}",
                }
            ],
        ]
        return ButtonsWithText(text="Выберите время:", buttons=buttons)

    def _get_confirm_notification_data(self, callback_data):
        data = callback_data.call_data.split()[2:]
        hour, minute = data[0].split(":")[1].split("-")
        token = data[1].split(":")[-1]
        user = models.TelegramUser.objects.get(telegram_id=callback_data.user_id)
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
            buttons=[[{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}]],
        )

    def _get_notification_data(self, callback_data):
        user = models.TelegramUser.objects.get(telegram_id=callback_data.user_id)
        if user.action == "NONE":
            return ButtonsWithText(
                text=settings.MESSAGES["NOT_ADDED_TOKEN_FOR_UNPIN_RU"],
                buttons=[
                    [{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}]
                ],
            )

        return ButtonsWithText(
            text=settings.MESSAGES["ABOUT_NOTIFICATION_RU"].format(
                token=user.token.username, date=f"{str(user.notification_time)[:5]}"
            ),
            buttons=[
                [
                    {
                        "text": settings.MESSAGES["CONFIRM_DELETE_NOTIFICATION_RU"],
                        "callback_data": "confirm-delete",
                    }
                ],
                [{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}],
            ],
        )

    def _get_confirm_delete_notification_data(self, callback_data):
        user = models.TelegramUser.objects.get(telegram_id=callback_data.user_id)
        user.action = "NONE"
        user.token = None
        user.notification_time = None
        user.save(update_fields=["action", "token", "notification_time"])
        return ButtonsWithText(
            text=settings.MESSAGES["SUCCESS_DELETE_NOTIFICATION_RU"],
            buttons=[[{"text": settings.MESSAGES["MENU_RU"], "callback_data": "menu"}]],
        )

    def _get_data_time_menu(self, callback_data):
        data = callback_data.call_data.split()
        hour, minute = data[1].split(":")[1].split("-")
        return self._get_time_for_notification_data(callback_data, h=hour, m=minute)

    def _get_data(self, callback_data):
        return self._get_quickstart_data()

    def _send_callback(self, callback_data, is_menu=False):
        data: ButtonsWithText
        if is_menu:
            data = self._handle_callback_for_menu(callback_data)
        else:
            data = self._handle_callback(callback_data)

        requests.get(
            settings.API_URL_TELEGRAM + "/editMessageText",
            params={
                "chat_id": callback_data.user_id,
                "text": data.text,
                "message_id": callback_data.message_id,
                "reply_markup": json.dumps({"inline_keyboard": data.buttons}),
            },
        )

    def _delete_token(self, callback_data):
        token = callback_data.call_data.split(":")[1]
        token = models.CustomUser.objects.filter(username=token).first()
        models.TelegramUserToken.objects.filter(
            token__username=token.username,
            telegram_user__telegram_id=callback_data.user_id,
        ).delete()

    def _add_token(self, callback_data):
        token = callback_data.call_data.split(":")[1]
        token = models.CustomUser.objects.get(username=token)
        user = models.TelegramUser.objects.get(telegram_id=callback_data.user_id)
        models.TelegramUserToken.objects.create(token=token, telegram_user=user)

    @staticmethod
    def is_callback(callback):
        try:
            _ = callback["callback_query"]["from"]["id"]
            return True
        except KeyError:
            return False

    def _handle_callback(self, callback_data):
        """The order of conditions is important"""

        if callback_data.call_data.startswith("M"):
            return self._handle_callback_for_menu(callback_data)
        if callback_data.call_data == "menu":
            return self.get_settings()
        elif callback_data.call_data == "help":
            return self._get_help_data()
        elif callback_data.call_data in ("tokens", "menu-tokens"):
            return self._get_tokens_data()
        elif callback_data.call_data == "quickstart":
            return self._get_quickstart_data()

        elif callback_data.call_data == "add":
            return self._get_add_data()

        elif callback_data.call_data in ("favorites", "menu-favorites"):
            return self._get_favorites_data(callback_data, call_data="about-token-self")

        elif callback_data.call_data in ("pin", "menu-pin"):  # Choice group
            return self._get_tokens_for_notification_data(callback_data)
        elif callback_data.call_data.startswith("menu-time"):  # Choice group
            return self._get_data_time_menu(callback_data)

        elif callback_data.call_data.startswith("confirm-not"):  # Confirm notification
            return self._get_confirm_notification_data(callback_data)
        elif re.search("(minus|plus)", callback_data.call_data):  # Choice time
            return self._change_time_for_notification_data(callback_data)
        elif "pin-time" in callback_data.call_data:  # Choice action
            return self._get_action_for_notification_data(callback_data)
        elif "pin-token" in callback_data.call_data:  # Choice token
            return self._get_time_for_notification_data(callback_data)

        elif callback_data.call_data == "unpin":
            return self._get_notification_data(callback_data)
        elif callback_data.call_data == "confirm-delete":
            return self._get_confirm_delete_notification_data(callback_data)

        elif callback_data.call_data.startswith("about-token"):  # TODO: done
            return self._get_about_token_data(callback_data)

        elif re.match(r"(del-token|add-token)", callback_data.call_data):  # TODO: done
            if callback_data.call_data.startswith("del"):
                self._delete_token(callback_data)
            else:
                self._add_token(callback_data)

            if "self" in callback_data.call_data:
                return self._get_about_token_data(callback_data, favorites_token=True)
            return self._get_about_token_data(callback_data)

    def _get_data_for_buttons_of_menu(self, data, callback_data):
        token = callback_data.call_data.split(":")[-1]
        return ButtonsWithText(
            text=data,
            buttons=[
                [
                    {
                        "text": settings.MESSAGES["MENU_TOKENS_RU"],
                        "callback_data": f"MainMenu:{token}",
                    }
                ]
            ],
        )

    def _get_number_week(self):
        return f"Номер недели - {self._time_service.get_week_number() + 1}"

    def _get_data_for_today_and_tomorrow_paris(self, callback_data, day, week):
        token = callback_data.call_data.split(":")[-1]
        instances = api_models.Schedule.objects.filter(
            group__username=token,
            week__name__startswith=week,
            day__name__iexact=day.name,
        ).order_by("number_pair")
        result = f"{day.name.title()}\n\n"
        for inst in instances:
            result += (
                f"{inst.number_pair}) {inst.subject} {inst.teacher} {inst.audience}\n"
            )
        return result

    def _get_pairs(self, callback_data, is_today=True):
        day = self._time_service.get_week_day()
        week = self._time_service.get_week_number()
        if is_today and day.num == 6:
            return "Сегодня выходной :)"
        if not is_today and day.num == 5:
            return "Завтра выходной :)"
        if not is_today and day.num == 6:
            week = 0 if week + 1 == 4 else week + 1
        if not is_today:
            day = self._time_service.get_week_day(is_today=False)

        return self._get_data_for_today_and_tomorrow_paris(
            callback_data, day, str(week)
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
        week = str(self._time_service.get_week_number())
        instances = api_models.Schedule.objects.filter(
            group__username=token, week__name__startswith=week
        ).order_by(*["day_id", "number_pair"])
        if len(instances):
            first_day = instances[0].day.name
            result = f"{first_day}\n"
            for s in instances:
                if s.day.name != first_day:
                    first_day = s.day.name
                    result += f"\n{first_day}\n"
                result += f"{s.number_pair}) {s.subject} {s.type_pair.name} {s.teacher} {s.audience}\n"
            return result
        return "Нет данных :("

    def _handle_callback_for_menu(self, callback_data):
        """The order of conditions is important"""

        data = None
        if callback_data.call_data == "MainMenu":
            return self.get_menu(callback_data)
        if callback_data.call_data.startswith("MainMenu:"):
            return self.get_menu_buttons(callback_data)
        elif callback_data.call_data.startswith("MB-number-week"):
            data = self._get_number_week()
        elif callback_data.call_data.startswith("MB-pairs-today"):
            data = self._get_pairs(callback_data)
        elif callback_data.call_data.startswith("MB-pairs-tomorrow"):
            data = self._get_pairs(callback_data, is_today=False)
        elif callback_data.call_data.startswith("MB-teachers"):
            data = self._get_teachers(callback_data)
        elif callback_data.call_data.startswith("MB-subjects"):
            data = self._get_subjects(callback_data)
        elif callback_data.call_data.startswith("MB-schedule"):
            data = self._get_schedule(callback_data)
        if data is not None:
            return self._get_data_for_buttons_of_menu(data, callback_data)

    def send_callback(self, callback_data):
        self._send_callback(callback_data)
