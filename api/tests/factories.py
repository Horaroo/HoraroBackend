import factory.fuzzy
from factory.django import DjangoModelFactory

from api.models import Event, Type
from users.models import CustomUser, TelegramUser


class BaseUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser


class ActiveUserFactory(BaseUserFactory):
    username = factory.Sequence(lambda n: "username_{}".format(n))


class TelegramUserFactory(DjangoModelFactory):
    class Meta:
        model = TelegramUser


class TypeFactory(DjangoModelFactory):
    class Meta:
        model = Type


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    title = "Event title"
    description = "Description for event"
