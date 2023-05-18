from django.db import models


class TelegramUser(models.Model):
    ACTION_CHOICES = (
        ("PTY", "PairsToday"),
        ("PTW", "PairsTomorrow"),
        ("NONE", "none"),
    )

    username = models.TextField(default="Username doesn't exists")
    telegram_id = models.TextField(unique=True)
    is_moder = models.BooleanField(default=False)
    type_chat = models.CharField(max_length=255, blank=True, null=True)
    token = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Token of notifications",
    )
    action = models.CharField(
        max_length=4, choices=ACTION_CHOICES, default="NONE"
    )
    notification_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.telegram_id
