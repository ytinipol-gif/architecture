from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status

from app import storage
from app.auth import create_token, get_current_user
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
    description="REST API для управления пользователями, событиями и регистрациями",
)


@app.get("/", response_model=MessageResponse, tags=["Сервис"])
def root():
    return {"message": "Сервис успешно запущен"}


#Аутентификация

@app.post(
    "/api/v1/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Аутентификация"],
    summary="Регистрация пользователя",
)
def register_user(request: UserRegisterRequest):
    # проверяю, есть ли уже пользователь с таким логином
    found_user = None
    for u in storage.users:
        if u["login"] == request.login:
            found_user = u
            break

    if found_user:
        raise HTTPException(status_code=409, detail="Пользователь с таким логином уже существует")

    # создаю нового пользователя
    user = {
        "id": storage.user_id_seq,
        "login": request.login,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "email": request.email,
        "password": request.password,
    }

    storage.users.append(user)
    storage.user_id_seq += 1

    return {
        "id": user["id"],
        "login": user["login"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
    }


@app.post(
    "/api/v1/auth/login",
    response_model=TokenResponse,
    tags=["Аутентификация"],
    summary="Вход пользователя",
)
def login_user(request: UserLoginRequest):
    # ищем пользователя по логину и паролю
    user = None
    for u in storage.users:
        if u["login"] == request.login and u["password"] == request.password:
            user = u
            break

    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    return {"access_token": create_token(user), "token_type": "bearer"}


#Пользоватекли

@app.get(
    "/api/v1/users/by-login",
    response_model=UserResponse,
    tags=["Пользователи"],
    summary="Поиск пользователя по логину",
)
def get_user_by_login(login: str = Query(...)):
    user = None
    for u in storage.users:
        if u["login"] == login:
            user = u
            break

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return {
        "id": user["id"],
        "login": user["login"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
    }


@app.get(
    "/api/v1/users/search",
    response_model=List[UserResponse],
    tags=["Пользователи"],
    summary="Поиск пользователей по имени или фамилии",
)
def search_users(mask: str = Query(...)):
    result = []

    for u in storage.users:
        if mask.lower() in u["first_name"].lower() or mask.lower() in u["last_name"].lower():
            result.append(
                {
                    "id": u["id"],
                    "login": u["login"],
                    "first_name": u["first_name"],
                    "last_name": u["last_name"],
                    "email": u["email"],
                }
            )

    return result


#События

@app.post(
    "/api/v1/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["События"],
    summary="Создание события",
)
def create_event(request: EventCreateRequest, current_user: dict = Depends(get_current_user)):
    event = {
        "id": storage.event_id_seq,
        "title": request.title,
        "description": request.description,
        "date": request.date,
        "location": request.location,
        "organizer_id": current_user["id"],
    }

    storage.events.append(event)
    storage.event_id_seq += 1

    return event


@app.get(
    "/api/v1/events",
    response_model=List[EventResponse],
    tags=["События"],
    summary="Получение списка событий",
)
def get_events():
    return storage.events


@app.get(
    "/api/v1/events/by-date",
    response_model=List[EventResponse],
    tags=["События"],
    summary="Поиск событий по дате",
)
def get_events_by_date(date: str = Query(...)):
    result = []
    for e in storage.events:
        if e["date"] == date:
            result.append(e)
    return result


#Регистрация

@app.post(
    "/api/v1/events/{event_id}/registrations",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Регистрации"],
    summary="Регистрация пользователя на событие",
)
def register_for_event(event_id: int, current_user: dict = Depends(get_current_user)):
    # поиск события
    event = None
    for e in storage.events:
        if e["id"] == event_id:
            event = e
            break

    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")

    # проверяю, не зарегистрирован ли уже пользователь
    existing = None
    for r in storage.registrations:
        if r["event_id"] == event_id and r["user_id"] == current_user["id"]:
            existing = r
            break

    if existing:
        raise HTTPException(status_code=409, detail="Пользователь уже зарегистрирован")

    from datetime import datetime

    registration = {
        "user_id": current_user["id"],
        "event_id": event_id,
        "registration_date": datetime.utcnow().isoformat(),
        "status": "зарегистрирован",
    }

    storage.registrations.append(registration)

    return registration


@app.get(
    "/api/v1/events/{event_id}/participants",
    response_model=List[UserResponse],
    tags=["Регистрации"],
    summary="Получение участников события",
)
def get_event_participants(event_id: int, current_user: dict = Depends(get_current_user)):
    # проверяю, что событие существует
    event = None
    for e in storage.events:
        if e["id"] == event_id:
            event = e
            break

    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")

    # собираю id пользователей
    user_ids = []
    for r in storage.registrations:
        if r["event_id"] == event_id:
            user_ids.append(r["user_id"])

    result = []
    for u in storage.users:
        if u["id"] in user_ids:
            result.append(
                {
                    "id": u["id"],
                    "login": u["login"],
                    "first_name": u["first_name"],
                    "last_name": u["last_name"],
                    "email": u["email"],
                }
            )

    return result


@app.get(
    "/api/v1/users/me/events",
    response_model=List[EventResponse],
    tags=["Регистрации"],
    summary="Получение событий пользователя",
)
def get_my_events(current_user: dict = Depends(get_current_user)):
    event_ids = []

    for r in storage.registrations:
        if r["user_id"] == current_user["id"]:
            event_ids.append(r["event_id"])

    result = []
    for e in storage.events:
        if e["id"] in event_ids:
            result.append(e)

    return result


@app.delete(
    "/api/v1/events/{event_id}/registrations/me",
    response_model=MessageResponse,
    tags=["Регистрации"],
    summary="Отмена регистрации",
)
def cancel_registration(event_id: int, current_user: dict = Depends(get_current_user)):
    registration = None

    for r in storage.registrations:
        if r["event_id"] == event_id and r["user_id"] == current_user["id"]:
            registration = r
            break

    if not registration:
        raise HTTPException(status_code=404, detail="Регистрация не найдена")

    storage.registrations.remove(registration)

    return {"message": "Регистрация отменена"}