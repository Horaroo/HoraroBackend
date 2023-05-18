import datetime

import pytest

from api.tests import factories


@pytest.mark.django_db
def test_create_schedule(logged_user, logged_client):
    type_ = factories.TypeFactory(name="lc")
    day = factories.DayFactory(name="monday")
    week = factories.WeekFactory(name="1 week")

    response = logged_client.post(
        path="/api/v1/schedule/",
        data={
            "number_pair": 1,
            "subject": "test",
            "teacher": "teacher",
            "audience": "555 aud.",
            "week": week.name,
            "group": logged_user.username,
            "type_pair": type_.name,
            "day": day.name,
        },
    )

    assert response.status_code == 201
    assert len(response.json()) == 10


@pytest.mark.django_db
def test_schedule_copy_week(logged_client, logged_user):
    source_week = factories.WeekFactory(name="1")
    target_week = factories.WeekFactory(name="2")
    pair_time = datetime.datetime.now()
    subject = factories.ScheduleFactory(
        subject="Subject for week 1",
        week=source_week,
        start_time=pair_time,
        end_time=pair_time,
        group=logged_user,
    )
    target_day = factories.ScheduleFactory(
        subject="Subject for week 2",
        week=target_week,
        group=logged_user,
    )

    response = logged_client.post(
        "/api/v1/schedule/copy/",
        data={
            "source_week": source_week.name,
            "target_week": target_week.name,
        },
    )

    result = logged_client.get(
        f"/api/v1/get-pair/{target_week.name}/{target_day.day.name}/1/?token={logged_user.username}"
    )
    assert response.status_code == 201

    assert result.json()["start_time"][:10] == str(pair_time)[:10]
    assert result.json()["end_time"][:10] == str(pair_time)[:10]
    assert result.json()["subject"] == subject.subject


@pytest.mark.django_db
def test_schedule_copy_day(logged_client, logged_user):
    day_tuesday = factories.DayFactory(name="tuesday")
    day_friday = factories.DayFactory(name="friday")
    subject_monday = factories.ScheduleFactory(
        subject="Subject for Monday", group=logged_user
    )
    factories.ScheduleFactory(
        subject="Subject for Tuesday",
        group=logged_user,
        day=day_tuesday,
    )
    subject_friday = factories.ScheduleFactory(
        subject="Subject for Friday",
        group=logged_user,
        day=day_friday,
    )

    response = logged_client.post(
        "/api/v1/schedule/copy/",
        data={
            "source_week": subject_monday.week.name,
            "target_week": subject_monday.week.name,
            "source_day": subject_monday.day.name,
            "target_day": subject_friday.day.name,
        },
    )
    result = logged_client.get(
        f"/api/v1/get-pair/{subject_monday.week.name}/{subject_friday.day.name}/1/?token={logged_user.username}"
    )

    assert response.status_code == 201

    assert result.status_code == 200
    data = result.json()

    assert data["subject"] == subject_monday.subject


@pytest.mark.django_db
def test_schedule_detail_field(logged_user, logged_client):
    schedule = factories.ScheduleFactory(
        teacher="teacher",
        group=logged_user,
    )
    response = logged_client.get(
        "/api/v1/schedule/detail/{}/?teacher=true&q=tea".format(
            logged_user.username
        )
    )

    assert response.status_code == 200
    assert response.json()["results"][0]["name"] == schedule.teacher


@pytest.mark.django_db
def test_get_schedule_one_field(logged_user, logged_client):
    schedule = factories.ScheduleFactory(
        teacher="test teacher",
        group=logged_user,
    )

    response = logged_client.get(
        "/api/v1/schedule/get_one_field/?token={}&select_field=teacher".format(
            logged_user.username
        )
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["teacher"] == schedule.teacher


@pytest.mark.django_db
def test_get_pair_schedule(logged_user, logged_client):
    subject = factories.ScheduleFactory(
        subject="subject",
        group=logged_user,
    )
    response = logged_client.get(
        "/api/v1/get-pair/{week}/{day}/{number}/?token={token}".format(
            week=subject.week.name,
            day=subject.day.name,
            number=1,
            token=logged_user.username,
        )
    )

    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == subject.subject
    assert data["number_pair"] == subject.number_pair
    assert data["teacher"] == subject.teacher


@pytest.mark.django_db
def test_delete_pair_schedule(logged_user, logged_client):
    subject = factories.ScheduleFactory(
        group=logged_user,
    )
    response = logged_client.delete(
        "/api/v1/get-pair/{week}/{day}/{number}/?token={token}".format(
            week=subject.week.name,
            day=subject.day.name,
            number=1,
            token=logged_user.username,
        )
    )

    assert response.status_code == 204


@pytest.mark.django_db
def test_get_type_pair(not_logged_client):
    factories.TypeFactory.create_batch(name="lecture", size=10)

    response = not_logged_client.get("/api/v1/type-pair/")

    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.django_db
def test_schedule_copy_pair(logged_client, logged_user):
    day_tuesday = factories.DayFactory(name="tuesday")
    day_friday = factories.DayFactory(name="friday")
    subject_monday = factories.ScheduleFactory(
        subject="Subject for Monday", group=logged_user
    )
    factories.ScheduleFactory(
        subject="Subject for Tuesday",
        group=logged_user,
        day=day_tuesday,
    )
    subject_friday = factories.ScheduleFactory(
        subject="Subject for Friday",
        group=logged_user,
        day=day_friday,
        number_pair=2,
    )
    target_pair = 2
    response = logged_client.post(
        "/api/v1/schedule/copy/",
        data={
            "source_week": subject_monday.week.name,
            "target_week": subject_monday.week.name,
            "source_day": subject_monday.day.name,
            "target_day": subject_friday.day.name,
            "source_pair": subject_monday.number_pair,
            "target_pair": target_pair,
        },
    )
    week_name = subject_monday.week.name
    day_name = subject_friday.day.name
    result = logged_client.get(
        f"/api/v1/get-pair/{week_name}/{day_name}/{target_pair}/?token={logged_user.username}"
    )

    assert response.status_code == 201

    assert result.status_code == 200
    data = result.json()

    assert data["subject"] == subject_monday.subject


@pytest.mark.django_db
def test_update_schedule(logged_user, logged_client):
    type_ = factories.TypeFactory(name="lc")
    day = factories.DayFactory(name="monday")
    week = factories.WeekFactory(name="1 week")
    schedule = factories.ScheduleFactory(
        subject="chemistry",
        teacher="same teacher",
        group=logged_user,
        day=day,
        week=week,
        type_pair=type_,
    )
    response = logged_client.post(
        path="/api/v1/schedule/",
        data={
            "number_pair": 1,
            "subject": "biology",
            "teacher": "same teacher",
            "audience": "555 aud.",
            "week": week.name,
            "group": logged_user.username,
            "type_pair": type_.name,
            "day": day.name,
        },
    )

    assert response.status_code == 201
    assert len(response.json()) == 10

    assert response.json()["teacher"] == schedule.teacher
    assert response.json()["subject"] == "biology"
