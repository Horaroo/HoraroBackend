import dataclasses
from typing import Union

from django.db.models import QuerySet

from schedules import models
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

    @staticmethod
    def _delete_instances(instances: QuerySet):
        if instances:
            instances.delete()

    def _get_target_week(self):
        return models.Week.objects.filter(name__exact=self.target_week).first()

    def _get_target_day(self):
        return models.Day.objects.filter(name__exact=self.target_day).first()

    def _copy_week(self):
        instances = self.queryset.filter(
            group__username=self.user.username, week__name=self.target_week
        )
        self._delete_instances(instances)

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
        self._delete_instances(instances)

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
        instance = self.queryset.filter(
            group__username=self.user.username,
            week__name=self.target_week,
            day__name=self.target_day,
            number_pair=self.target_pair,
        )
        self._delete_instances(instance)
        instance = self.queryset.filter(
            group__username=self.user.username,
            week__name=self.source_week,
            day__name=self.source_day,
            number_pair=self.source_pair,
        )
        if instance:
            target_week = self._get_target_week()
            target_day = self._get_target_day()
            instance = instance.first()
            self.queryset.create(
                group=instance.group,
                week=target_week,
                day=target_day,
                number_pair=self.target_pair,
                subject=instance.subject,
                teacher=instance.teacher,
                audience=instance.audience,
                type_pair=instance.type_pair,
                start_time=instance.start_time,
                end_time=instance.end_time,
            )

    def execute(self):
        if all(
            (
                self.source_pair,
                self.target_pair,
                self.target_day,
                self.source_day,
            )
        ):
            self._copy_pair()
        elif all((self.source_day, self.target_day)):
            self._copy_day()
        else:
            self._copy_week()
