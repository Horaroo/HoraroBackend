from datetime import date, datetime
from zoneinfo import ZoneInfo



from django.conf import settings


import requests
from celery import shared_task

from api.models import Schedule
from api.time.configs.constants import WEEK_DAYS_RU
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
    for user in qs_users:
        week_day, week_number = _get_week_data(user.action)
        temp = {
            "telegram_id": user.telegram_id,
            "action": user.action,
            "token": user.token.username,
            "data": Schedule.objects.filter(
                group=user.token.pk,
                week__name__startswith=week_number,
                day__name__icontains=week_day,
            ).order_by("number_pair"),
        }
        notification_data.append(temp)

    result = []

    for not_data in notification_data:
        if not_data["action"] == "PTY" and time_service.get_week_day().num == 6:
            continue
        if not_data["action"] == "PTW" and time_service.get_week_day().num == 5:
            continue
        result.append(_parse_data(not_data))

    return result


def _parse_data(not_data) -> dict:
    data = not_data["data"]
    token = not_data["token"]
    result = settings.MESSAGES["TITLE_NOTIFICATION_RU"].format(token=token)
    for pair in data:
        result += f"{pair.number_pair}) {pair.subject} {pair.type_pair.name} {pair.audience}\n"

    return {"telegram_id": not_data["telegram_id"], "text": result}




def _get_week_data(action):
    week_day_num = time_service.get_week_day().num
    week_number = time_service.get_week_number()
    if action == "PTW":
        week_day_num = (week_day_num + 1) % 7
        if week_day_num == 0:
            week_number = (week_number + 1) % 4
    return WEEK_DAYS_RU[week_day_num], str(week_number)
