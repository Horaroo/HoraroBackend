import factory.fuzzy
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User


class BaseUserFactory(DjangoModelFactory):
    class Meta:
        model = User


class ActiveUserFactory(BaseUserFactory):
    username = factory.Sequence(lambda n: 'username_{}'.format(n))
