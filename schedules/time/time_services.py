from datetime import datetime

from django.forms.models import model_to_dict

from schedules.models import Schedule
from schedules.time.configs.constants import (
    DSTU_SCHEDULE_TIME,
    RU_MSC_TZ,
    WEEK_DAYS_EN,
    WEEK_DAYS_RU,
    WEEK_DAYS_TOMORROW_EN,
    WEEK_DAYS_TOMORROW_RU,
)
from schedules.time.configs.dataclasses import PairStatus, Time, TimeRange, WeekDay


def _pair_model_to_dict(pair: Schedule) -> dict:
    fields = ["subject", "teacher", "audience", "week", "group", "type_pair", "day"]
    return model_to_dict(pair, fields=fields)


class TimeServices:
    def get_week_day(self, lang: str = "ru", tz=RU_MSC_TZ, is_today=True) -> WeekDay:
        if lang not in ["ru", "en"]:
            raise ValueError(f"This language is not provided: {lang}")

        week_day_num = datetime.now(tz=tz).weekday()
        if is_today:
            if lang.lower() == "en":
                week_day = WEEK_DAYS_EN[week_day_num]
            else:
                week_day = WEEK_DAYS_RU[week_day_num]
            week_day_rus = WEEK_DAYS_RU[week_day_num]
        else:
            if lang.lower() == "en":
                week_day = WEEK_DAYS_TOMORROW_EN[week_day_num]
            else:
                week_day = WEEK_DAYS_TOMORROW_RU[week_day_num]
            week_day_rus = WEEK_DAYS_TOMORROW_RU[week_day_num]

        return WeekDay(num=week_day_num, name=week_day, rus_name=week_day_rus)

    def get_current_time(self, tz=RU_MSC_TZ, second=False):
        if second:
            return str(datetime.now(tz=tz))[:19]
        cur_time = Time(
            hour=datetime.now(tz=tz).hour, minute=datetime.now(tz=tz).minute
        )
        return cur_time

    def get_start_date(self) -> datetime:
        """In future will receive it from db"""
        return datetime(day=1, month=2, year=2023)

    def get_week_number(self, date=None) -> int:
        """Returns week number [0-3]"""
        start_date = self.get_start_date()
        start_date_week_day = start_date.weekday()
        if date is None:
            date = datetime.now()
        days_count = (date - start_date).days

        return (days_count + start_date_week_day) // 7 % 4

    def get_pair_status(self, time: Time = None) -> PairStatus:
        """
        Returns pair status bound to time
        but not bound to data from database
        """
        # In future will receive pair times from db
        schedule = DSTU_SCHEDULE_TIME
        if time is None:
            time = self.get_current_time()

        pairs = list(schedule.values())

        if time < pairs[0].start:
            return PairStatus(status="early", pair_num=0, time_range=schedule[0])
        for pair_num, time_range in enumerate(pairs):
            if time in time_range:
                return PairStatus(
                    status="pair", pair_num=pair_num, time_range=schedule[pair_num]
                )

        breaks = [
            TimeRange(start=pairs[i - 1].end, end=pairs[i].start)
            for i in range(1, len(pairs))
        ]
        for break_num, _break in enumerate(breaks):
            if time in _break:
                return PairStatus(
                    status="break",
                    pair_num=break_num + 1,
                    time_range=schedule[break_num + 1],
                )
        return PairStatus(status="nothing")

    def get_current_pair(self, pair_qs, time: Time = None) -> PairStatus:
        schedule = DSTU_SCHEDULE_TIME
        if time is None:
            time = self.get_current_time()

        pair_status = self.get_pair_status(time)
        if pair_status.status == "nothing":
            return PairStatus(status="nothing", pair_num=None)
        if (
            pair_status.pair_num + 1 < pair_qs[0].number_pair
            or pair_status.pair_num + 1 == pair_qs[0].number_pair
            and pair_status.status == "break"
        ):
            return PairStatus(
                status="early",
                pair_num=pair_qs[0].number_pair,
                pair_data=_pair_model_to_dict(pair_qs[0]),
                time_range=schedule[pair_qs[0].number_pair - 1],
            )
        for pair in pair_qs:
            if pair.number_pair == pair_status.pair_num + 1:
                if pair_status.status == "break":
                    return PairStatus(
                        status="break",
                        pair_num=pair.number_pair,
                        pair_data=_pair_model_to_dict(pair),
                        time_range=schedule[pair.number_pair - 1],
                    )
                if pair_status.status == "pair":
                    return PairStatus(
                        status="pair",
                        pair_num=pair.number_pair,
                        pair_data=_pair_model_to_dict(pair),
                        time_range=schedule[pair.number_pair - 1],
                    )


if __name__ == "__main__":
    ts = TimeServices()
    # print(ts.get_week_number(datetime(day=25, month=9, year=2022)))
    # pair = ts.get_pair_status(time=Time(hour=15, minute=0))
    # print(pair.to_dict())
