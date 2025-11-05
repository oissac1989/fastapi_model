from http import HTTPStatus

from fastapi_model.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "johndoe",
            "email": "teste@gmail.com",
            "password": "strongpassword123",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "johndoe",
        "email": "teste@gmail.com",
        "id": 1,
    }


def test_create_user_conflict_username(client, add_user):
    response = client.post(
        "/users/",
        json={
            "username": "existinguser",
            "email": "teste@gmail.com",
            "password": "password123",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already registered"}


def test_create_user_conflict_email(client, add_user):
    response = client.post(
        "/users/",
        json={
            "username": "newuser",
            "email": "teste@gmail.com",
            "password": "password123",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already registered"}


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_existing_user(client, add_user):
    user_schema = UserPublic.model_validate(add_user).model_dump()
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, add_user):
    response = client.put(
        "/users/1",
        json={
            "username": "existinguser",
            "email": "teste@gmail.com",
            "password": "password123",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "existinguser",
        "email": "teste@gmail.com",
        "id": 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        "/users/999",
        json={
            "username": "nonexistent",
            "email": "teste@gmail.com",
            "password": "strongpassword123",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_integrity_error(client, add_user):
    # Criando um registro para "fausto"
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f"/users/{add_user.id}",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {"detail": "Username or Email already exists"}


def test_delete_user(client, add_user):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_found(client):
    response = client.delete("/users/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
