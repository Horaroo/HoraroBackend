from django.contrib.sites.models import Site
from django.db import models


class ContentSlide(models.Model):
    title = models.TextField()
    description = models.TextField()
    image = models.ImageField(blank=True)
    cover_image = models.ImageField(blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def picture(self):
        if self.image:
            return Site.objects.get_current().domain + "/" + self.image.name
        else:
            return None

    def cover(self):
        if self.cover_image:
            return Site.objects.get_current().domain + "/" + self.cover_image.name
        else:
            return None
