import datetime

import factory.fuzzy
from factory import faker
from factory.django import DjangoModelFactory

from schedules.models import Day, Schedule, Type, Week
from users.models import CustomUser, TelegramUser


class BaseUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = faker.Faker("email")


class ActiveUserFactory(BaseUserFactory):
    username = factory.Sequence(lambda n: "username_{}".format(n))


class TelegramUserFactory(DjangoModelFactory):
    class Meta:
        model = TelegramUser


class TypeFactory(DjangoModelFactory):
    class Meta:
        model = Type

    name = "lc."


class DayFactory(DjangoModelFactory):
    class Meta:
        model = Day

    name = "monday"


class WeekFactory(DjangoModelFactory):
    class Meta:
        model = Week

    name = "1"


class ScheduleFactory(DjangoModelFactory):
    class Meta:
        model = Schedule

    day = factory.SubFactory(DayFactory)
    group = factory.SubFactory(ActiveUserFactory)
    type_pair = factory.SubFactory(TypeFactory)
    week = factory.SubFactory(WeekFactory)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    teacher = "Some teacher"
    subject = "Some subject"
    audience = "555 aud."
    number_pair = 1
