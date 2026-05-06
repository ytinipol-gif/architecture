import os

os.environ["CACHE_USE_MEMORY"] = "1"
os.environ["RATE_LIMIT_USE_MEMORY"] = "1"

import mongomock
from fastapi.testclient import TestClient

from app import cache, database, rate_limit

test_database = mongomock.MongoClient()["events_db_test"]
database.set_test_database(test_database)

from app.main import app

client = TestClient(app)


def setup_function():
    for name in test_database.list_collection_names():
        test_database[name].drop()
    cache.reset_cache_backend()
    rate_limit.reset_rate_backend()
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


def test_reregister_after_cancel():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Повторная регистрация",
            "description": "Проверка повторной регистрации после отмены",
            "date": "2026-04-20",
            "location": "Москва",
        },
    )

    first_registration = client.post("/api/v1/events/1/registrations", headers=headers)
    cancel_response = client.delete("/api/v1/events/1/registrations/me", headers=headers)
    second_registration = client.post("/api/v1/events/1/registrations", headers=headers)

    assert first_registration.status_code == 201
    assert cancel_response.status_code == 200
    assert second_registration.status_code == 201
    assert second_registration.json()["status"] == "registered"


def test_events_cache_headers():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Кешируемое событие",
            "description": "Проверка кеширования списка событий",
            "date": "2026-04-21",
            "location": "Москва",
        },
    )

    first_response = client.get("/api/v1/events")
    second_response = client.get("/api/v1/events")

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.headers["X-Cache"] == "MISS"
    assert second_response.headers["X-Cache"] == "HIT"


def test_cache_invalidation_after_registration():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Митап по кешу",
            "description": "Проверка инвалидации кеша после регистрации",
            "date": "2026-04-22",
            "location": "Москва",
        },
    )

    first_response = client.get("/api/v1/events/1/participants", headers=headers)
    register_response = client.post("/api/v1/events/1/registrations", headers=headers)
    second_response = client.get("/api/v1/events/1/participants", headers=headers)

    assert first_response.status_code == 200
    assert register_response.status_code == 201
    assert second_response.status_code == 200
    assert first_response.headers["X-Cache"] == "MISS"
    assert second_response.headers["X-Cache"] == "MISS"
    assert len(second_response.json()) == 1


def test_login_rate_limit():
    register_user(login="rate_user", email="rate_user@mail.ru")

    last_response = None
    for _ in range(6):
        last_response = client.post(
            "/api/v1/auth/login",
            json={
                "login": "rate_user",
                "password": "123456",
            },
        )

    assert last_response is not None
    assert last_response.status_code == 429
    assert "X-RateLimit-Limit" in last_response.headers
    assert "X-RateLimit-Remaining" in last_response.headers
    assert "X-RateLimit-Reset" in last_response.headers
