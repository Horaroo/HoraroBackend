import dataclasses

from schedules.models import Schedule
from schedules.time.configs.constants import WEEK_DAYS_RU
from schedules.time.time_services import TimeServices
from users.models import TelegramUser


@dataclasses.dataclass
class NotificationGetter:
    hour: int | None
    minute: int | None
    _time_service: TimeServices = TimeServices()

    def _get_week_data(self, action):
        week_day_num = self._time_service.get_week_day().num
        week_number = self._time_service.get_week_number()
        if action == "PTW":
            week_day_num = (week_day_num + 1) % 7
            if week_day_num == 0:
                week_number = (week_number + 1) % 4
        return WEEK_DAYS_RU[week_day_num], str(week_number)

    def _get_current_time(self):
        hour = self._time_service.get_current_time().hour
        minute = self._time_service.get_current_time().minute
        if self.hour is not None and self.minute is not None:
            hour, minute = self.hour, self.minute

        return hour, minute

    def execute(self):
        hour, minute = self._get_current_time()

        qs_users = TelegramUser.objects.filter(
            notification_time=hour, notification_time_min=minute
        )

        result = []
        for user in qs_users:
            week_day, week_number = self._get_week_data(user.action)
            temp = {
                "telegram_id": user.telegram_id,
                "action": user.action,
                "group": user.token.group,
                "data": Schedule.objects.filter(
                    group=user.token.pk,
                    week__name__startswith=week_number,
                    day__name__icontains=week_day,
                ).order_by("number_pair"),
            }
            result.append(temp)

        return result
