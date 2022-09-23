import factory.fuzzy
from factory.django import DjangoModelFactory
from users.models import CustomUser, TelegramUser, GroupUserTelegram


class BaseUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser


class ActiveUserFactory(BaseUserFactory):
    username = factory.Sequence(lambda n: 'username_{}'.format(n))


class TelegramUserFactory(DjangoModelFactory):
    class Meta:
        model = TelegramUser


class GroupUserTelegramFactory(DjangoModelFactory):
    class Meta:
        model = GroupUserTelegram
