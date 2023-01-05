import pytest

from api.tests import factories


@pytest.mark.django_db
def test_get_event_list(not_logged_client):
    factories.EventFactory.create_batch(size=2)

    response = not_logged_client.get("/api/v1/events/")

    assert response.status_code == 200
    assert len(response.json()) == 2
