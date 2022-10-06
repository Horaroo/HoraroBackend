import pytest
from .factories import *


@pytest.mark.django_db
def test_telegram_detail_user_post(not_logged_client):
    response = not_logged_client.post('/api/v1/telegram/detail/user/', data={'telegram_id': '123456',
                                                                             'username': 'name'})

    assert response.status_code == 201
    assert len(response.json()) == 3


@pytest.mark.django_db
def test_telegram_detail_user_get_user_moder(not_logged_client):
    TelegramUserFactory(username="test1",
                        is_moder=True)
    TelegramUserFactory(username="test2",
                        is_moder=True,
                        telegram_id=321)
    TelegramUserFactory(username="test3",
                        is_moder=False,
                        telegram_id=123)

    response = not_logged_client.get('/api/v1/telegram/detail/user/?is_moder=true')

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.django_db
def test_telegram_detail_user_get_user_not_moder(not_logged_client):
    TelegramUserFactory(username="test1",
                        is_moder=True)
    TelegramUserFactory(username="test2",
                        is_moder=True,
                        telegram_id=321)
    TelegramUserFactory(username="test3",
                        is_moder=False,
                        telegram_id=123)

    response = not_logged_client.get('/api/v1/telegram/detail/user/?is_moder=false')

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_telegram_detail_user_get_user_list(not_logged_client):
    TelegramUserFactory(username="test1",
                        is_moder=True)
    TelegramUserFactory(username="test2",
                        is_moder=True,
                        telegram_id=321)
    TelegramUserFactory(username="test3",
                        is_moder=False,
                        telegram_id=123)

    response = not_logged_client.get('/api/v1/telegram/detail/user/')

    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.django_db
def test_telegram_detail_group_list_user(not_logged_client):
    CustomUser.objects.create(username="test",
                              password="password",
                              email="test@example.com",
                              group="test")

    user_telegram = TelegramUser.objects.create(telegram_id="1234567",
                                                username="test")
    TelegramUser.objects.create(telegram_id="11234567",
                                username="test1")
    group = GroupUserTelegramFactory(token="test")
    list_users = TelegramUser.objects.filter(telegram_id__istartswith='1').all()
    group.user.set(list_users)

    response = not_logged_client.get('/api/v1/telegram/detail/group/?telegram_id={}'.format(user_telegram.telegram_id))
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_add_token(not_logged_client):
    CustomUser.objects.create(username="test",
                              password="password",
                              email="test@example.com",
                              group="test")

    TelegramUser.objects.create(telegram_id="11234567",
                                username="test1")

    response = not_logged_client.post('/api/v1/telegram/detail/group/', data={
        "group": "test",
        "token": "test",
        "telegram_id": "11234567"
    })
    assert response.status_code == 201
    assert len(response.json()) == 2


@pytest.mark.django_db
def test_del_token(not_logged_client):
    CustomUser.objects.create(username="test",
                              password="password",
                              email="test@example.com",
                              group="test")

    telegram_user = TelegramUser.objects.create(telegram_id="11234567",
                                                username="test1")
    TelegramUser.objects.create(telegram_id="131234567",
                                username="test1")

    group = GroupUserTelegramFactory(token="test")
    list_users = TelegramUser.objects.filter(telegram_id__istartswith='1').all()
    group.user.set(list_users)
    response = not_logged_client.delete('/api/v1/telegram/detail/group/?telegram_id={}&token={}'.format(
        telegram_user.telegram_id,
        "test"
    ))
    assert response.status_code == 204


@pytest.mark.django_db
def test_get_all_group(not_logged_client):
    CustomUser.objects.create(username="test1",
                              password="passw",
                              group="test1",
                              email="test1@example.com")
    CustomUser.objects.create(username="test2",
                              password="passw",
                              group="test2",
                              email="test2@example.com")

    response = not_logged_client.get("/api/v1/list/group/")

    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.test
@pytest.mark.django_db
def test_telegram_detail_user_update(not_logged_client):
    telegram_user = TelegramUserFactory(username="test1",
                                        is_moder=True)
    user = CustomUser.objects.create(username="test2",
                                     password="passw",
                                     group="test2",
                                     email="test2@example.com")
    payload = {
        "action": "PWT",
        "token": user.username,
        "notification_time": 9
    }

    response = not_logged_client.patch('/api/v1/telegram/detail/user/{}/'.format(telegram_user.pk),
                                       payload)
    telegram_user.refresh_from_db()

    assert response.status_code == 200
    assert telegram_user.action == payload.get('action')
    assert telegram_user.token == payload.get('token')
    assert telegram_user.notification_time == payload.get('notification_time')

    # token = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    # action = models.CharField(choices=ACTION_CHOICES, blank=True, null=True)
    # notification_time = models.IntegerField(blank=True, null=True)
