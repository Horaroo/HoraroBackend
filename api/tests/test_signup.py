import pytest


@pytest.mark.django_db
def test_register(logged_client, name, group, telegram_id):

    assert logged_client.get(f'/api/v1/user/{telegram_id}/', data={'telegram_id': True}).status_code == 404
    assert logged_client.get(f'/api/v1/user/{name}/', data={'user': True}).status_code == 404
    assert logged_client.get(f'/api/v1/user/{group}/').status_code == 404

    pyload = dict(
        username=name,
        password="password",
        telegram_id=telegram_id,
        group=group
    )
    r = logged_client.post(f'/api/v1/register/', data={'username': pyload['username'],
                                                       'password': pyload['password'],
                                                       'telegram_id': pyload['telegram_id'],
                                                       'group': pyload['group']})

    assert r.status_code == 200

