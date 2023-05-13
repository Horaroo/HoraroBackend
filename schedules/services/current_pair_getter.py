import dataclasses

from django.shortcuts import get_object_or_404

from schedules.models import Schedule
from schedules.time.configs.dataclasses import Time
from schedules.time.time_services import TimeServices
from users.models import CustomUser


@dataclasses.dataclass
class CurrentPairGetter:
    token: str
    h: int | None
    m: int | None
    _time_service: TimeServices = TimeServices()

    def get_queryset(self):
        group = get_object_or_404(CustomUser, username=self.token)
        week_day = self._time_service.get_week_day().name
        week_number = str(self._time_service.get_week_number())

        return Schedule.objects.filter(
            group=group,
            week__name__startswith=week_number,
            day__name__icontains=week_day,
        ).order_by("number_pair")

    def execute(self):
        if self.h is not None and self.m is not None:
            time = Time(hour=int(self.h), minute=int(self.m))
        else:
            time = None

        qs = self.get_queryset()
        current_pair = self._time_service.get_current_pair(qs, time=time)
        return current_pair.to_dict()
