from django.db import models

from schedules import models as schedule_models
from users.models import CustomUser


class Schedule(models.Model):
    number_pair = models.IntegerField(blank=True, null=True)
    subject = models.TextField()
    teacher = models.TextField()
    audience = models.TextField()
    week = models.ForeignKey(schedule_models.Week, on_delete=models.CASCADE)
    group = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_pair = models.ForeignKey(schedule_models.Type, on_delete=models.CASCADE)
    day = models.ForeignKey(schedule_models.Day, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f"{self.number_pair}: {self.subject} - {self.group.group}"
