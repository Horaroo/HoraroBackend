import factory.fuzzy
from factory.django import DjangoModelFactory
from users.models import CustomUser


class BaseUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser


class ActiveUserFactory(BaseUserFactory):
    username = factory.Sequence(lambda n: 'username_{}'.format(n))
