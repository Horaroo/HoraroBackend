from zoneinfo import ZoneInfo

from .dataclasses import Time, TimeRange

WEEK_DAYS_RU = {
    0: "понедельник",
    1: "вторник",
    2: "среда",
    3: "четверг",
    4: "пятница",
    5: "суббота",
    6: "воскресенье",
}

WEEK_DAYS_TOMORROW_RU = {
    6: "понедельник",
    0: "вторник",
    1: "среда",
    2: "четверг",
    3: "пятница",
    4: "суббота",
    5: "воскресенье",
}

WEEK_DAYS_EN = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}

WEEK_DAYS_TOMORROW_EN = {
    6: "monday",
    0: "tuesday",
    1: "wednesday",
    2: "thursday",
    3: "friday",
    4: "saturday",
    5: "sunday",
}

RU_MSC_TZ = ZoneInfo("Europe/Moscow")

DSTU_SCHEDULE_TIME = {
    0: TimeRange(start=Time(hour=8, minute=30), end=Time(hour=10, minute=0)),
    1: TimeRange(start=Time(hour=10, minute=10), end=Time(hour=11, minute=40)),
    2: TimeRange(start=Time(hour=12, minute=20), end=Time(hour=13, minute=50)),
    3: TimeRange(start=Time(hour=14, minute=0), end=Time(hour=15, minute=30)),
}
