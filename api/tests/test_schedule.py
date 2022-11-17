import pytest
from api.models import Schedule, Type, Day, Week
from api.tests.factories import TypeFactory
import datetime


@pytest.mark.django_db
def test_create_schedule(logged_user, logged_client):
    type_ = Type.objects.create(name="lc")
    day = Day.objects.create(name="monday")
    week = Week.objects.create(name="1 week")

    response = logged_client.post(path='/api/v1/schedule/', data={
        "number_pair": 1,
        "subject": "test",
        "teacher": "teacher",
        "audience": "555 aud.",
        "week": week.pk,
        "group": logged_user.pk,
        "type_pair": type_.pk,
        "day": day.pk
    })

    assert response.status_code == 201
    assert len(response.json()) == 10

@pytest.mark.test
@pytest.mark.django_db
def test_schedule_copy_week(logged_user, logged_client):
    type_ = Type.objects.create(name="lc")
    day = Day.objects.create(name="monday")
    week1 = Week.objects.create(name="1 week")
    week2 = Week.objects.create(name="2 week")
    pair_time = datetime.datetime.now()
    schedule = Schedule.objects.create(
        number_pair=1,
        subject='subject',
        teacher='teacher',
        audience='555 aud.',
        week=week1,
        day=day,
        group=logged_user,
        type_pair=type_,
        start_time=pair_time,
        end_time=pair_time
    )

    response = logged_client.post('/api/v1/schedule/copy-week/',
                                  data={
                                      "username": logged_user.username,
                                      "from_week": week1.pk,
                                      "to_week": week2.pk
                                  })
    result = logged_client.get(f'/api/v1/get-pair/{week2.pk}/{day.pk}/1/?token={logged_user.username}')

    assert response.status_code == 201
    assert result.json()['start_time'][:10] == str(pair_time)[:10]
    assert result.json()['end_time'][:10] == str(pair_time)[:10]


@pytest.mark.django_db
def test_schedule_detail_field(logged_user, logged_client):
    type_ = Type.objects.create(name="lc")
    day = Day.objects.create(name="monday")
    week = Week.objects.create(name="1 week")
    schedule = Schedule.objects.create(
        number_pair=1,
        subject='subject',
        teacher='teacher',
        audience='555 aud.',
        week=week,
        day=day,
        group=logged_user,
        type_pair=type_
    )
    response = logged_client.get('/api/v1/schedule/detail/{}/?teacher=true&q=tea'.format(logged_user.username))

    assert response.status_code == 200
    assert response.json()['results'][0]['name'] == schedule.teacher


@pytest.mark.django_db
def test_get_schedule_one_field(logged_user, logged_client):
    type_ = Type.objects.create(name="lc")
    day = Day.objects.create(name="monday")
    week = Week.objects.create(name="1 week")
    schedule = Schedule.objects.create(
        number_pair=1,
        subject='subject',
        teacher='test teacher',
        audience='555 aud.',
        week=week,
        day=day,
        group=logged_user,
        type_pair=type_
    )

    response = logged_client.get(
        '/api/v1/schedule/get_one_field/?token={}&select_field=teacher'.format(logged_user.username))

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['teacher'] == schedule.teacher


@pytest.mark.django_db
def test_get_pair_schedule(logged_user, logged_client):
    day = Day.objects.create(name="monday")
    week = Week.objects.create(name="1 week")
    type_ = Type.objects.create(name="lc")
    Schedule.objects.create(
        number_pair=1,
        subject='subject',
        teacher='test teacher',
        audience='555 aud.',
        week=week,
        day=day,
        group=logged_user,
        type_pair=type_
    )
    response = logged_client.get("/api/v1/get-pair/{week}/{day}/{number}/?token={token}"
                                 .format(week=week.pk, day=day.pk, number=1, token=logged_user.username))

    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.django_db
def test_delete_pair_schedule(logged_user, logged_client):
    type_ = Type.objects.create(name="lc")
    day = Day.objects.create(name="monday")
    week = Week.objects.create(name="1 week")
    Schedule.objects.create(
        number_pair=1,
        subject='subject',
        teacher='test teacher',
        audience='555 aud.',
        week=week,
        day=day,
        group=logged_user,
        type_pair=type_
    )
    response = logged_client.delete("/api/v1/get-pair/{week}/{day}/{number}/?token={token}"
                                    .format(week=week.pk, day=day.pk, number=1, token=logged_user.username))

    assert response.status_code == 204


@pytest.mark.django_db
def test_get_type_pair(not_logged_client):
    TypeFactory.create_batch(name="lecture", size=10)

    response = not_logged_client.get("/api/v1/type-pair/")

    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.skip
@pytest.mark.django_db
def test_get_schedule_list(logged_user, logged_client):
    pass
