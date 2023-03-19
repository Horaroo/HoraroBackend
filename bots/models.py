from django.db import models


class EventCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
