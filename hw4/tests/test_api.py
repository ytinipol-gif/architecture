import mongomock
from fastapi.testclient import TestClient

from app import database

test_database = mongomock.MongoClient()["events_db_test"]
database.set_test_database(test_database)

from app.main import app

client = TestClient(app)


def setup_function():
    for name in test_database.list_collection_names():
        test_database[name].drop()
    database.ensure_indexes()


def register_user(login="maria_lemeshchenko", email="maria@mail.ru"):
    return client.post(
        "/api/v1/auth/register",
        json={
            "login": login,
            "first_name": "Мария",
            "last_name": "Лемещенко",
            "email": email,
            "password": "123456",
        },
    )


def login_user(login="maria_lemeshchenko"):
    return client.post(
        "/api/v1/auth/login",
        json={
            "login": login,
            "password": "123456",
        },
    )


def auth_headers():
    register_user()
    response = login_user()
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_user():
    response = register_user()
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_login_user():
    register_user()
    response = login_user()
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_event():
    headers = auth_headers()
    response = client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Архитектурный митап",
            "description": "Встреча по архитектуре приложений",
            "date": "2026-04-20",
            "location": "Москва",
        },
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_register_for_event():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Архитектурный митап",
            "description": "Встреча по архитектуре приложений",
            "date": "2026-04-20",
            "location": "Москва",
        },
    )
    response = client.post("/api/v1/events/1/registrations", headers=headers)
    assert response.status_code == 201
    assert response.json()["status"] == "registered"


def test_cancel_registration():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Архитектурный митап",
            "description": "Встреча по архитектуре приложений",
            "date": "2026-04-20",
            "location": "Москва",
        },
    )
    client.post("/api/v1/events/1/registrations", headers=headers)
    response = client.delete("/api/v1/events/1/registrations/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Регистрация отменена"

