from rest_framework.test import APIClient

import pytest

from api.tests import factories


@pytest.fixture
def logged_user(db):
    return factories.ActiveUserFactory()


@pytest.fixture
def logged_client(logged_user):
    client = APIClient()
    client.force_authenticate(logged_user)
    return client


@pytest.fixture
def not_logged_client():
    client = APIClient()
    return client


@pytest.fixture(autouse=True)
def mock_things(settings):
    settings.DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
    settings.THUMBNAIL_STORAGE = "inmemorystorage.InMemoryStorage"
