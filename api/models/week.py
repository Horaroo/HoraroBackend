from django.contrib.sites.models import Site
from django.db import models

from users.models import CustomUser


class Week(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name