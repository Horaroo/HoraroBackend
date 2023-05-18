from django.db import models

from users.models import CustomUser

from .day import Day
from .type_pair import Type
from .week import Week


class Schedule(models.Model):
    number_pair = models.IntegerField(blank=True, null=True)
    subject = models.TextField()
    teacher = models.TextField()
    audience = models.TextField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    group = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_pair = models.ForeignKey(Type, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time = models.DateTimeField(
        auto_now_add=False, null=True, blank=True
    )
    end_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f"{self.number_pair}: {self.subject} - {self.group.group}"
