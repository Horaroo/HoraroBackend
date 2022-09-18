import pytest
from rest_framework.test import APIClient
from api.tests import factories


@pytest.fixture
def logged_user(db):
    return factories.ActiveUserFactory()


@pytest.fixture
def logged_client(logged_user):
    client = APIClient()
    client.force_authenticate(logged_user)
    return client
