import pytest


@pytest.mark.skip
@pytest.mark.django_db
def test_user_sign_up(not_logged_client):

    response = not_logged_client.post(path='/api/v1/auth/detail/users/', data={
        "username": "some_name",
        "password": "some_password",
        "group": "some_group",
        "email": "some_email@mail.com"
    })

    assert response.status_code == 201
    assert len(response.json()) == 5
