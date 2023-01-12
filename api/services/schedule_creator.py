import dataclasses

from django.db.models import Q

from api import models


@dataclasses.dataclass
class ScheduleCreatorOrUpdater:
    data: dict

    def _create(self):
        return models.Schedule.objects.create(**self.data)

    def _update(self):
        group = self.data["group"]
        number = self.data["number_pair"]
        week = self.data["week"]
        day = self.data["day"]
        obj = models.Schedule.objects.filter(
            Q(number_pair=number) & Q(week=week) & Q(group=group) & Q(day=day)
        )

        if bool(obj):
            instance = obj.first()
            for attr, value in self.data.items():
                setattr(instance, attr, value)

            if self.data.get("start_time"):
                new_time = self.data.get("start_time")
                for inst in models.Schedule.objects.filter(number_pair=number, group=group):
                    inst.start_time = new_time
                    inst.save()
            if self.data.get("end_time"):
                new_time = self.data.get("end_time")
                for inst in models.Schedule.objects.filter(number_pair=number, group=group):
                    inst.end_time = new_time
                    inst.save()
            instance.save()
            return instance
        return self._create()

    def execute(self):
        return self._update()
