import dataclasses

from schedules.models import Schedule


@dataclasses.dataclass
class ScheduleWeekGetter:
    token: str
    week: str

    def execute(self):
        data = []
        for i in range(1, 7):
            qs = Schedule.objects.filter(
                group__username=self.token,
                week__name__startswith=self.week,
                day_id=i,
            ).order_by("number_pair")
            if qs:
                data.append(
                    [
                        f"{elem.number_pair}) {elem.subject} {elem.type_pair} {elem.teacher} {elem.audience} "
                        f'{str(elem.start_time.hour + 3) + ":" + str(elem.start_time.minute) + " - " + str(elem.end_time.hour + 3) + ":" + str(elem.end_time.minute) if bool(elem.start_time and elem.end_time) else ""}'
                        for elem in qs
                    ]
                )
            else:
                data.append([])
        return data
