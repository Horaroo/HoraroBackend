from django.db import models
from users.models import CustomUser


class NumberWeek(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)


class Week(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Day(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    number_pair = models.IntegerField()
    subject = models.TextField()
    teacher = models.TextField()
    audience = models.TextField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    group = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_pair = models.ForeignKey(Type, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number_pair}: {self.subject} - {self.group.group.name}'


