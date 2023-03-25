import dataclasses

from django.db.models import Q

from api import models
from users.models import CustomUser


@dataclasses.dataclass
class ScheduleCreatorOrUpdater:
    data: dict

    def _create(self):
        week = models.Week.objects.filter(
            name=self.data.pop("week").get("name")
        ).first()
        day = models.Day.objects.filter(name=self.data.pop("day").get("name")).first()
        group = CustomUser.objects.filter(
            username=self.data.pop("group").get("username")
        ).first()
        type_pair = models.Type.objects.filter(
            name=self.data.pop("type_pair").get("name")
        ).first()
        return models.Schedule.objects.create(
            week=week, day=day, group=group, type_pair=type_pair, **self.data
        )

    def _update_time(self, number, group):
        if self.data.get("start_time"):
            new_time = self.data.get("start_time")
            models.Schedule.objects.filter(number_pair=number, group=group).update(
                start_time=new_time
            )
        if self.data.get("end_time"):
            new_time = self.data.get("start_time")
            models.Schedule.objects.filter(number_pair=number, group=group).update(
                start_time=new_time
            )

    def _update(self):
        group = self.data["group"]
        number = self.data["number_pair"]
        week = self.data["week"]
        day = self.data["day"]
        obj = models.Schedule.objects.filter(
            Q(number_pair=number)
            & Q(week__name=week)
            & Q(group__username=group)
            & Q(day__name=day)
        )

        if bool(obj):
            instance = obj.first()
            for attr, value in self.data.items():
                setattr(instance, attr, value)
            instance.save()
        else:
            instance = self._create()
        self._update_time(number, group)
        return instance

    def execute(self):
        return self._update()
