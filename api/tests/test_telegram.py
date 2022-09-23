import pytest
from api.tests.factories import TelegramUserFactory, GroupUserTelegramFactory


@pytest.mark.django_db
def test_telegram_detail_user_post(not_logged_client):
    response = not_logged_client.post(path='/api/v1/telegram/detail/user/', data={'telegram_id': '123456',
                                                                                  'username': 'name'})

    assert response.status_code == 201
    assert len(response.json()) == 3

