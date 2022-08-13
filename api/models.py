from django.db import models
from users.models import CustomUser


class NumberWeek(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return self.number


class Schedules(models.Model):
    class Meta:
        verbose_name_plural = 'schedules'
    first_monday = models.TextField(default='Поле не заполнено')
    first_tuesday = models.TextField(default='Поле не заполнено')
    first_wednesday = models.TextField(default='Поле не заполнено')
    first_thursday = models.TextField(default='Поле не заполнено')
    first_friday = models.TextField(default='Поле не заполнено')
    first_saturday = models.TextField(default='Поле не заполнено')
    second_monday = models.TextField(default='Поле не заполнено')
    second_tuesday = models.TextField(default='Поле не заполнено')
    second_wednesday = models.TextField(default='Поле не заполнено')
    second_thursday = models.TextField(default='Поле не заполнено')
    second_friday = models.TextField(default='Поле не заполнено')
    second_saturday = models.TextField(default='Поле не заполнено')
    third_monday = models.TextField(default='Поле не заполнено')
    third_tuesday = models.TextField(default='Поле не заполнено')
    third_wednesday = models.TextField(default='Поле не заполнено')
    third_thursday = models.TextField(default='Поле не заполнено')
    third_friday = models.TextField(default='Поле не заполнено')
    third_saturday = models.TextField(default='Поле не заполнено')
    fourth_monday = models.TextField(default='Поле не заполнено')
    fourth_tuesday = models.TextField(default='Поле не заполнено')
    fourth_wednesday = models.TextField(default='Поле не заполнено')
    fourth_thursday = models.TextField(default='Поле не заполнено')
    fourth_friday = models.TextField(default='Поле не заполнено')
    fourth_saturday = models.TextField(default='Поле не заполнено')
    group = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.group.group


