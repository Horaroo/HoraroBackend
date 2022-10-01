import dataclasses
from dataclasses import dataclass
from typing import Literal


@dataclass
class Time:
    hour: int
    minute: int

    def __lt__(self, other: 'Time'):
        if self.hour < other.hour:
            return True
        elif self.hour == other.hour and self.minute < other.minute:
            return True
        else:
            return False

    def __le__(self, other: 'Time'):
        if self.hour < other.hour:
            return True
        elif self.hour == other.hour and self.minute <= other.minute:
            return True
        else:
            return False


@dataclass
class WeekDay:
    num: int
    name: str


@dataclass
class TimeRange:
    start: Time
    end: Time

    def __contains__(self, item: Time):
        return self.start <= item <= self.end


@dataclass
class PairStatus:
    """
    status - show is it pair now or break, or nothing
    pair_num - '0' if status is 'early'
               current pair number if status is 'pair'
               next pair number if status is 'break'
               None if status break
    """
    status: Literal['early', 'pair', 'break', 'nothing']
    pair_num:  int | None = None
    pair_data: dict | None = None
    time_range: TimeRange | None = None

    def to_dict(self):
        return dataclasses.asdict(self)


