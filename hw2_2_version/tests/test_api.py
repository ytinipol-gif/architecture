from fastapi.testclient import TestClient
from app.main import app
from app import storage

client = TestClient(app)

# перед каждым тестом очищаю хранилище
def setup_function():
    storage.users.clear()
    storage.events.clear()
    storage.registrations.clear()
    storage.user_id_seq = 1
    storage.event_id_seq = 1

# перед каждым тестом очищаю хранилище
def register_user(login="maria", email="maria@example.com"):
    return client.post(
        "/api/v1/auth/register",
        json={
            "login": login,
            "first_name": "Мария",
            "last_name": "Лемешенко",
            "email": email,
            "password": "123456",
        },
    )


def login_user(login="maria"):
    return client.post(
        "/api/v1/auth/login",
        json={
            "login": login,
            "password": "123456",
        },
    )


def auth_headers(login="maria", email="maria@example.com"):
    register_user(login=login, email=email)
    response = login_user(login=login)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_user_success():
    response = register_user()
    assert response.status_code == 201
    data = response.json()
    assert data["login"] == "maria"
    assert data["first_name"] == "Мария"


def test_register_user_conflict():
    register_user()
    response = register_user()
    assert response.status_code == 409


def test_login_success():
    register_user()
    response = login_user()
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_create_event_unauthorized():
    response = client.post(
        "/api/v1/events",
        json={
            "title": "Тест",
            "description": "Описание",
            "date": "2026-03-25",
            "location": "Москва",
        },
    )
    assert response.status_code == 401


def test_create_event_success():
    headers = auth_headers()
    response = client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Тест событие",
            "description": "Описание",
            "date": "2026-03-25",
            "location": "Москва",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тест событие"
    assert data["organizer_id"] == 1


def test_get_events_success():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Архитектурный митап",
            "description": "Обсуждение архитектуры",
            "date": "2026-03-25",
            "location": "Москва",
        },
    )

    response = client.get("/api/v1/events")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_register_for_event_success():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Архитектурный митап",
            "description": "Обсуждение архитектуры",
            "date": "2026-03-25",
            "location": "Москва",
        },
    )

    response = client.post("/api/v1/events/1/registrations", headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["event_id"] == 1
    assert data["user_id"] == 1


def test_register_for_event_conflict():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Архитектурный митап",
            "description": "Обсуждение архитектуры",
            "date": "2026-03-25",
            "location": "Москва",
        },
    )

    client.post("/api/v1/events/1/registrations", headers=headers)
    response = client.post("/api/v1/events/1/registrations", headers=headers)
    assert response.status_code == 409


def test_get_participants_success():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Архитектурный митап",
            "description": "Обсуждение архитектуры",
            "date": "2026-03-25",
            "location": "Москва",
        },
    )
    client.post("/api/v1/events/1/registrations", headers=headers)

    response = client.get("/api/v1/events/1/participants", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["login"] == "maria"


def test_get_my_events_success():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Архитектурный митап",
            "description": "Обсуждение архитектуры",
            "date": "2026-03-25",
            "location": "Москва",
        },
    )
    client.post("/api/v1/events/1/registrations", headers=headers)

    response = client.get("/api/v1/users/me/events", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_cancel_registration_success():
    headers = auth_headers()
    client.post(
        "/api/v1/events",
        headers=headers,
        json={
            "title": "Архитектурный митап",
            "description": "Обсуждение архитектуры",
            "date": "2026-03-25",
            "location": "Москва",
        },
    )
    client.post("/api/v1/events/1/registrations", headers=headers)

    response = client.delete("/api/v1/events/1/registrations/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Регистрация отменена"