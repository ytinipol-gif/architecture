from datetime import datetime, timezone
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status

from app.auth import create_token, get_current_user
from app.database import ensure_indexes, get_database, get_next_sequence
from app.schemas import (
    EventCreateRequest,
    EventResponse,
    MessageResponse,
    RegistrationResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)

app = FastAPI(
    title="Система управления событиями",
    version="1.0.0",
    description="REST API для управления пользователями, событиями и регистрациями на MongoDB",
)

ensure_indexes()


def user_to_response(user: dict) -> dict:
    return {
        "id": user["id"],
        "login": user["login"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
    }


def event_to_response(event: dict) -> dict:
    return {
        "id": event["id"],
        "title": event["title"],
        "description": event["description"],
        "date": event["event_date"].strftime("%Y-%m-%d"),
        "location": event["location"],
        "organizer_id": event["organizer_id"],
    }


@app.get("/", response_model=MessageResponse, tags=["Сервис"])
def root():
    return {"message": "Сервис успешно запущен"}


@app.post(
    "/api/v1/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Аутентификация"],
    summary="Регистрация пользователя",
)
def register_user(request: UserRegisterRequest):
    database = get_database()

    if database.users.find_one({"login": request.login}):
        raise HTTPException(status_code=409, detail="Пользователь с таким логином уже существует")

    if database.users.find_one({"email": request.email}):
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")

    user = {
        "id": get_next_sequence("users"),
        "login": request.login,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "email": request.email,
        "password_hash": request.password,
        "created_at": datetime.now(timezone.utc),
    }

    database.users.insert_one(user)
    return user_to_response(user)


@app.post(
    "/api/v1/auth/login",
    response_model=TokenResponse,
    tags=["Аутентификация"],
    summary="Вход пользователя",
)
def login_user(request: UserLoginRequest):
    user = get_database().users.find_one(
        {
            "login": request.login,
            "password_hash": request.password,
        }
    )

    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    return {"access_token": create_token(user), "token_type": "bearer"}


@app.get(
    "/api/v1/users/by-login",
    response_model=UserResponse,
    tags=["Пользователи"],
    summary="Поиск пользователя по логину",
)
def get_user_by_login(login: str = Query(...)):
    user = get_database().users.find_one({"login": login})
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user_to_response(user)


@app.get(
    "/api/v1/users/search",
    response_model=List[UserResponse],
    tags=["Пользователи"],
    summary="Поиск пользователей по имени или фамилии",
)
def search_users(mask: str = Query(...)):
    users = get_database().users.find(
        {
            "$or": [
                {"first_name": {"$regex": mask, "$options": "i"}},
                {"last_name": {"$regex": mask, "$options": "i"}},
            ]
        }
    ).sort([("last_name", 1), ("first_name", 1)])

    return [user_to_response(user) for user in users]


@app.post(
    "/api/v1/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["События"],
    summary="Создание события",
)
def create_event(request: EventCreateRequest, current_user: dict = Depends(get_current_user)):
    event = {
        "id": get_next_sequence("events"),
        "title": request.title,
        "description": request.description,
        "event_date": datetime.strptime(request.date, "%Y-%m-%d"),
        "location": request.location,
        "organizer_id": current_user["id"],
        "created_at": datetime.now(timezone.utc),
    }

    get_database().events.insert_one(event)
    return event_to_response(event)


@app.get(
    "/api/v1/events",
    response_model=List[EventResponse],
    tags=["События"],
    summary="Получение списка событий",
)
def get_events():
    events = get_database().events.find().sort([("event_date", 1), ("id", 1)])
    return [event_to_response(event) for event in events]


@app.get(
    "/api/v1/events/by-date",
    response_model=List[EventResponse],
    tags=["События"],
    summary="Поиск событий по дате",
)
def get_events_by_date(date: str = Query(...)):
    search_date = datetime.strptime(date, "%Y-%m-%d")
    events = get_database().events.find({"event_date": search_date}).sort("id", 1)
    return [event_to_response(event) for event in events]


@app.post(
    "/api/v1/events/{event_id}/registrations",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Регистрации"],
    summary="Регистрация пользователя на событие",
)
def register_for_event(event_id: int, current_user: dict = Depends(get_current_user)):
    database = get_database()

    event = database.events.find_one({"id": event_id})
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")

    existing = database.event_participants.find_one(
        {
            "event_id": event_id,
            "user_id": current_user["id"],
            "status": "registered",
        }
    )
    if existing:
        raise HTTPException(status_code=409, detail="Пользователь уже зарегистрирован")

    registration = {
        "id": get_next_sequence("event_participants"),
        "event_id": event_id,
        "user_id": current_user["id"],
        "registration_date": datetime.now(timezone.utc),
        "status": "registered",
    }

    database.event_participants.insert_one(registration)

    return {
        "user_id": registration["user_id"],
        "event_id": registration["event_id"],
        "registration_date": registration["registration_date"].isoformat(),
        "status": registration["status"],
    }


@app.get(
    "/api/v1/events/{event_id}/participants",
    response_model=List[UserResponse],
    tags=["Регистрации"],
    summary="Получение участников события",
)
def get_event_participants(event_id: int, current_user: dict = Depends(get_current_user)):
    del current_user
    database = get_database()

    event = database.events.find_one({"id": event_id})
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")

    registrations = list(
        database.event_participants.find(
            {
                "event_id": event_id,
                "status": "registered",
            }
        )
    )
    user_ids = [registration["user_id"] for registration in registrations]
    users = database.users.find({"id": {"$in": user_ids}}).sort([("last_name", 1), ("first_name", 1)])

    return [user_to_response(user) for user in users]


@app.get(
    "/api/v1/users/me/events",
    response_model=List[EventResponse],
    tags=["Регистрации"],
    summary="Получение событий пользователя",
)
def get_my_events(current_user: dict = Depends(get_current_user)):
    registrations = list(
        get_database().event_participants.find(
            {
                "user_id": current_user["id"],
                "status": "registered",
            }
        )
    )
    event_ids = [registration["event_id"] for registration in registrations]
    events = get_database().events.find({"id": {"$in": event_ids}}).sort([("event_date", 1), ("id", 1)])

    return [event_to_response(event) for event in events]


@app.delete(
    "/api/v1/events/{event_id}/registrations/me",
    response_model=MessageResponse,
    tags=["Регистрации"],
    summary="Отмена регистрации",
)
def cancel_registration(event_id: int, current_user: dict = Depends(get_current_user)):
    result = get_database().event_participants.update_one(
        {
            "event_id": event_id,
            "user_id": current_user["id"],
            "status": "registered",
        },
        {
            "$set": {
                "status": "cancelled",
            }
        },
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Регистрация не найдена")

    return {"message": "Регистрация отменена"}
