from django.contrib.auth.models import AbstractUser
from .validators import UnicodeUsernameValidator, email_validator
from django.db import models


class CustomUser(AbstractUser):

    username = models.CharField(
        max_length=15,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "Логин занят.",
        })

    group = models.CharField(max_length=15)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(models.EmailField.description,
                              unique=True,
                              validators=[email_validator],
                              error_messages={
                                  "unique": "Такая почта уже используется.",
                              })

    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class TelegramUser(models.Model):
    ACTION_CHOICES = (
        ('PTY', 'PairsToday'),
        ('PTW', 'PairsTomorrow'),
    )

    username = models.TextField()
    telegram_id = models.TextField(unique=True)
    is_moder = models.BooleanField(default=False)
    token = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)
    notification_time = models.IntegerField(blank=True, null=True, unique=False)

    def __str__(self):
        return self.telegram_id


class GroupUserTelegram(models.Model):
    """
    Было поздно ночью 1:31, решил написать такое, так как при изменении token и group полей, логику бота нужно
    переписывать, а на это времени сейчас пока что нет, с уважением Абулайсов А.
    """
    token = models.TextField()
    group = models.TextField()
    user = models.ManyToManyField(TelegramUser)
    owner_token = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.group}'

    def save(self, *args, **kwargs):
        self.owner_token = CustomUser.objects.get(username=self.token)
        super().save(*args, **kwargs)

