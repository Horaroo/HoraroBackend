import pytest

from ..models import Day, Schedule, Week
from .factories import *


@pytest.mark.django_db
def test_telegram_notifications(logged_user, logged_client):
    user = CustomUser.objects.create(
        username="test", password="password", email="test@example.com", group="test"
    )

    TelegramUser.objects.create(
        telegram_id="1234567",
        token=user,
        action="PTY",
        notification_time=21,
        notification_time_min=19,
    )
    TelegramUser.objects.create(
        telegram_id="2131324",
        token=user,
        action="PTW",
        notification_time=21,
        notification_time_min=23,
    )
    TelegramUser.objects.create(
        telegram_id="23424124",
        token=user,
        action="PTY",
        notification_time=19,
        notification_time_min=19,
    )

    type_ = Type.objects.create(name="lc")
    day = Day.objects.create(name="Суббота")
    week = Week.objects.create(name="2 week")
    Schedule.objects.create(
        number_pair=1,
        subject="subject",
        teacher="teacher",
        audience="555 aud.",
        week=week,
        day=day,
        group=user,
        type_pair=type_,
    )
    Schedule.objects.create(
        number_pair=1,
        subject="subject",
        teacher="teacher",
        audience="555 aud.",
        week=Week.objects.create(name="3 week"),
        day=day,
        group=user,
        type_pair=type_,
    )

    response = logged_client.get(
        "/api/v1/telegram/detail/user/notifications/?h=19&m=19"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
