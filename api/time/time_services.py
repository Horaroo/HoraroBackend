from datetime import datetime
from api.time.configs.dataclasses import WeekDay, Time, TimeRange, PairStatus
from api.time.configs.constants import (
    WEEK_DAYS_RU,
    WEEK_DAYS_EN,
    RU_MSC_TZ,
    DSTU_SCHEDULE_TIME)


class TimeServices:

    def get_week_day(self, lang: str = 'ru', tz=RU_MSC_TZ) -> WeekDay:
        if lang not in ['ru', 'en']:
            raise ValueError(f'This language is not provided: {lang}')

        week_day_num = datetime.now(tz=tz).weekday()
        if lang.lower() == 'en':
            week_day = WEEK_DAYS_EN[week_day_num]
        else:
            week_day = WEEK_DAYS_RU[week_day_num]

        return WeekDay(num=week_day_num, name=week_day)

    def get_current_time(self, tz=RU_MSC_TZ) -> Time:
        cur_time = Time(
            hour=datetime.now(tz=tz).hour,
            minute=datetime.now(tz=tz).minute
        )
        return cur_time

    def get_start_date(self) -> datetime:
        """In future will receive it from db"""
        return datetime(day=1, month=9, year=2022)

    def get_week_number(self, date=None) -> int:
        """ Returns week number [0-3] """
        start_date = self.get_start_date()
        start_date_week_day = start_date.weekday()
        if date is None:
            date = datetime.now()
        days_count = (date - start_date).days

        return (days_count + start_date_week_day + 2) // 7 % 4

    def get_pair_number(self, time: Time = None) -> PairStatus:
        """In future will receive pair times from db"""
        schedule = DSTU_SCHEDULE_TIME
        if time is None:
            time = self.get_current_time()

        pairs = list(schedule.items())
        breaks = [TimeRange(start=pairs[i - 1].end, end=pairs[i].start)
                  for i in range(1, len(pairs))]
        for pair_num, time_range in enumerate(pairs):
            if time in time_range:
                return PairStatus(status='pair', pair_num=pair_num)
        for break_num, _break in enumerate(breaks):
            if time in _break:
                return PairStatus(status='break', pair_num=break_num + 1)
        return PairStatus(status='nothing', pair_num=None)


if __name__ == '__main__':
    ts = TimeServices()
    wd_ru = ts.get_week_day(lang='ru')
    wd_en = ts.get_week_day(lang='en')
    _time = ts.get_current_time()
    week_number = ts.get_week_number(date=datetime(day=3, month=9, year=2022))
    print(
        wd_ru,
        wd_en,
        _time,
        week_number,
        sep='\n'
    )

    ts.get_pair_number(time=Time(hour=15, minute=31))

