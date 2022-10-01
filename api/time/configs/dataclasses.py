from dataclasses import dataclass
from typing import Literal

@dataclass
class Time:
    hour: int
    minute: int

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
    pair_num - 'first' if status is 'early'
               current pair number if status is 'pair'
               next pair number  if status is 'break'
               None if status break
    """
    status: Literal['early', 'pair', 'break', 'nothing']
    pair_num: Literal['First'] | int | None
