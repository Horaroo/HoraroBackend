from django.dispatch import receiver
from django.db.models.signals import post_save
from .views import telegram_service


@receiver(post_save, sender=None)
def send_event(sender, instance, **kwargs):
    telegram_service.event_sender(instance)
