import dataclasses
from typing import Any

from django.db.models import Q

from api import models


@dataclasses.dataclass
class ScheduleCreatorOrUpdater:
    data: dict
    serializer: Any

    def _create(self):
        return self.serializer.save()

    def _update(self):
        group = self.data["group"]
        number = self.data["number_pair"]
        week = self.data["week"]
        day = self.data["day"]
        obj = models.Schedule.objects.filter(
            Q(number_pair=number) & Q(week=week) & Q(group=group) & Q(day=day)
        )
        if obj.exists():
            obj.update(**self.data)
            new_time = self.data.get("start_time")
            end_time = self.data.get("end_time")
            if new_time or end_time:
                schedules = models.Schedule.objects.filter(
                    Q(number_pair=number) & Q(group__username=group)
                )
                if new_time:
                    schedules.update(start_time=new_time)
                if end_time:
                    schedules.update(end_time=end_time)

            return obj.first()
        return self._create()

    def execute(self):
        return self._update()
