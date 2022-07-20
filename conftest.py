import pytest
from rest_framework.test import RequestsClient, APIClient
from faker import Faker
from random import randint
from api.tests import factories


def _get_data(key_word):
    fake = Faker()
    return {'first_name': fake.first_name(), 'last_name': fake.last_name()}[key_word]


@pytest.fixture
def logged_user(db):
    return factories.ActiveUserFactory()


@pytest.fixture
def logged_client(logged_user):
    client = APIClient()
    client.force_authenticate(logged_user)
    return client


@pytest.fixture
def name():
    return _get_data('first_name')


@pytest.fixture
def telegram_id():
    return randint(10000, 1000000)


@pytest.fixture
def group():
    return _get_data('last_name')
