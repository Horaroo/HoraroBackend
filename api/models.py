from django.db import models
from users.models import CustomUser
from django.contrib.sites.models import Site


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
    number_pair = models.IntegerField(blank=True, null=True)
    subject = models.TextField()
    teacher = models.TextField()
    audience = models.TextField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    group = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_pair = models.ForeignKey(Type, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number_pair}: {self.subject} - {self.group.group}'


class Event(models.Model):
    title = models.TextField()
    description = models.TextField()
    image = models.ImageField(blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def picture(self):
        if self.image:
            return Site.objects.get_current().domain + '/' + self.image.name
        else:
            return None
