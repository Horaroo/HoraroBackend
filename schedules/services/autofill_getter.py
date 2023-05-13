import dataclasses

from django.db.models import F

from schedules.models import Schedule
from users.models import CustomUser


@dataclasses.dataclass
class AutofillGetter:
    query: str
    token: str
    field: dict

    def execute(self):
        group = CustomUser.objects.get(username=self.token)

        if self.field.get("teacher"):
            resp = Schedule.objects.filter(
                teacher__istartswith=self.query, group=group
            ).values(name=F("teacher"))
        elif self.field.get("subject"):
            resp = Schedule.objects.filter(
                subject__istartswith=self.query, group=group
            ).values(name=F("subject"))
        else:
            resp = Schedule.objects.filter(
                audience__istartswith=self.query, group=group
            ).values(name=F("audience"))

        return resp.distinct()
