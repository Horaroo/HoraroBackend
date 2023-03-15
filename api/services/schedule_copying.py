import dataclasses
from typing import Union

from django.db.models import QuerySet

from api import models
from users.models import CustomUser


@dataclasses.dataclass
class Copywriter:
    user: CustomUser
    queryset: QuerySet
    source_week: int
    target_week: int
    source_day: Union[str, None]
    target_day: Union[str, None]
    source_pair: Union[int, None]
    target_pair: Union[int, None]

    def _get_target_week(self):
        return models.Week.objects.filter(name__exact=self.target_week).first()

    def _get_target_day(self):
        return models.Day.objects.filter(name__exact=self.target_day).first()

    def _get_target_pair(self):
        pass

    def _copy_week(self):
        instances = self.queryset.filter(
            group__username=self.user.username, week__name=self.target_week
        )

        if instances:
            instances.delete()

        target_week = self._get_target_week()

        for data in self.queryset.filter(
            group__username=self.user.username, week__name=self.source_week
        ).all():
            self.queryset.create(
                number_pair=data.number_pair,
                subject=data.subject,
                teacher=data.teacher,
                audience=data.audience,
                week=target_week,
                group=data.group,
                type_pair=data.type_pair,
                day=data.day,
                start_time=data.start_time,
                end_time=data.end_time,
            )

    def _copy_day(self):
        instances = self.queryset.filter(
            group__username=self.user.username,
            week__name=self.target_week,
            day__name=self.target_day,
        )
        if instances:
            instances.delete()

        target_day = self._get_target_day()
        target_week = self._get_target_week()

        for data in self.queryset.filter(
            group__username=self.user.username,
            week__name=self.source_week,
            day__name=self.source_day,
        ):
            self.queryset.create(
                number_pair=data.number_pair,
                subject=data.subject,
                teacher=data.teacher,
                audience=data.audience,
                week=target_week,
                group=data.group,
                type_pair=data.type_pair,
                day=target_day,
                start_time=data.start_time,
                end_time=data.end_time,
            )

    def _copy_pair(self):
        pass

    def execute(self):
        if all((self.source_pair, self.target_pair, self.target_day, self.source_day)):
            self._copy_pair()
        elif all((self.source_day, self.target_day)):
            self._copy_day()
        else:
            self._copy_week()
