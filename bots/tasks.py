from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings

import requests
from celery import shared_task

from api.models import Schedule
from api.time.configs.constants import WEEK_DAYS_EN, WEEK_DAYS_RU
from api.time.time_services import TimeServices
from users.models import TelegramUser

tz = ZoneInfo("Europe/Moscow")
time_service = TimeServices()


@shared_task
def send_notification():
    current_time = datetime.now(tz=tz).hour, datetime.now(tz=tz).minute
    if current_time[1] % 5 == 0:
        telegram_users = TelegramUser.objects.filter(
            notification_time__hour=current_time[0],
            notification_time__minute=current_time[1],
        )
        notification_data = _get_data(telegram_users)
        for not_data in notification_data:
            requests.get(
                settings.API_URL_TELEGRAM + "/sendMessage",
                params={
                    "chat_id": not_data["telegram_id"],
                    "text": not_data["text"],
                    "parse_mode": "HTML",
                },
            )


def _get_data(qs_users) -> list[dict]:
    notification_data = []
    week_day_num = time_service.get_week_day().num
    for user in qs_users:
        if _skip_notification(user.action, week_day_num):
            continue
        week_day_n, week_number = _get_week_data(user.action)
        temp = {
            "telegram_id": user.telegram_id,
            "action": user.action,
            "token": user.token.username,
            "week_number": week_number,
            "data": Schedule.objects.filter(
                group=user.token.pk,
                week__name__startswith=week_number,
                day__name__iexact=WEEK_DAYS_EN[week_day_n],
            ).order_by("number_pair"),
        }
        notification_data.append(_parse_data(temp, week_day_n))

    return notification_data


def _parse_data(not_data, day_num) -> dict:
    data = not_data["data"]
    token = not_data["token"]
    action = f"Занятия на сегодня [{WEEK_DAYS_RU[day_num].title()}]: {not_data['week_number']} Неделя."
    if not_data["action"] == "PTW":
        action = f"Занятия на завтра [{WEEK_DAYS_RU[day_num].title()}]: {not_data['week_number']} Неделя."
    result = settings.MESSAGES["TITLE_NOTIFICATION_RU"].format(token=token)
    result += f"{action}\n\n"
    for pair in data:
        result += f"{pair.number_pair}) {pair.subject} {pair.teacher} {pair.type_pair.name} {pair.audience}\n"

    return {"telegram_id": not_data["telegram_id"], "text": result}


def _get_week_data(action):
    week_day_num = time_service.get_week_day().num
    week_number = time_service.get_week_number() + 1

    if action == "PTW":
        if week_day_num == 6:
            week_number = 1 if week_number + 1 == 5 else week_number + 1
        week_day_num = 0 if week_day_num + 1 == 7 else week_day_num + 1

    return week_day_num, str(week_number)


def _skip_notification(action, week_day_num):
    if action == "PTW" and week_day_num == 5:
        return True
    if action == "PTY" and week_day_num == 6:
        return True
