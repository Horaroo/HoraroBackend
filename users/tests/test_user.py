from unittest.mock import patch

import pytest


@patch("users.helpers.CustomActivationEmail.send")
@pytest.mark.django_db
def test_user_create(patched, not_logged_client):
    response = not_logged_client.post(
        path="/api/v1/auth/detail/",
        data={
            "username": "some_name",
            "password": "some_password",
            "group": "some_group",
            "email": "client@mail.com",
        },
    )

    assert response.status_code == 201
    assert len(response.json()) == 5
    assert patched.call_count == 1


@pytest.mark.django_db
def test_user_self_delete(logged_client, logged_user):
    logged_user.set_password("test")
    response = logged_client.delete(
        path="/api/v1/auth/detail/me/",
        data={"current_password": "test"},
    )
    assert response.status_code == 204


@pytest.mark.django_db
def test_user_self_get(logged_client, logged_user):
    response = logged_client.get(path="/api/v1/auth/detail/me/")
    assert response.status_code == 200
    assert response.json()["id"] == logged_user.pk


@pytest.mark.django_db
def test_user_self_update_username(logged_client, logged_user):
    response = logged_client.patch(
        path=f"/api/v1/auth/detail/{logged_user.username}/",
        data={"username": "new_username"},
    )
    logged_user.refresh_from_db()

    assert response.status_code == 200
    assert response.json()["username"] == logged_user.username


@pytest.mark.django_db
def test_user_delete_with_username(logged_client, logged_user):
    logged_user.set_password("test")
    response = logged_client.delete(
        path=f"/api/v1/auth/detail/{logged_user.username}/",
        data={"current_password": "test"},
    )

    assert response.status_code == 204


@pytest.mark.django_db
def test_create_auth_token_and_destroy(logged_client, logged_user):
    logged_user.is_active = True
    logged_user.email = "client@email.ru"
    logged_user.set_password("test")
    logged_user.save()

    response = logged_client.post(
        path="/api/v1/auth/token/login/",
        data={"email": logged_user.email, "password": "test"},
    )

    assert response.status_code == 200
    assert response.json()["auth_token"]
    assert int(response.json()["id"]) == logged_user.pk
    assert response.json()["username"] == logged_user.username

    response = logged_client.post("/api/v1/auth/token/logout/")

    assert response.status_code == 204
