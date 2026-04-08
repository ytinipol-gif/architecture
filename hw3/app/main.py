from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status

from app.auth import create_token, get_current_user
from app.db import get_connection
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

#АУТЕНТИФИКАЦИЯ
@app.post(
    "/api/v1/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Аутентификация"],
    summary="Регистрация пользователя",
)
def register_user(request: UserRegisterRequest):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM users
                WHERE login = %s
                """,
                (request.login,),
            )
            found_user = cur.fetchone()

            if found_user:
                raise HTTPException(status_code=409, detail="Пользователь с таким логином уже существует")

            cur.execute(
                """
                INSERT INTO users (login, first_name, last_name, email, password_hash)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, login, first_name, last_name, email
                """,
                (
                    request.login,
                    request.first_name,
                    request.last_name,
                    request.email,
                    request.password,
                ),
            )
            new_user = cur.fetchone()
            conn.commit()

    return {
        "id": new_user[0],
        "login": new_user[1],
        "first_name": new_user[2],
        "last_name": new_user[3],
        "email": new_user[4],
    }


@app.post(
    "/api/v1/auth/login",
    response_model=TokenResponse,
    tags=["Аутентификация"],
    summary="Вход пользователя",
)
def login_user(request: UserLoginRequest):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, login, first_name, last_name, email
                FROM users
                WHERE login = %s AND password_hash = %s
                """,
                (request.login, request.password),
            )
            user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    user_dict = {
        "id": user[0],
        "login": user[1],
        "first_name": user[2],
        "last_name": user[3],
        "email": user[4],
    }

    return {"access_token": create_token(user_dict), "token_type": "bearer"}


#ПОЛЬЗОВАТЕЛИ

@app.get(
    "/api/v1/users/by-login",
    response_model=UserResponse,
    tags=["Пользователи"],
    summary="Поиск пользователя по логину",
)
def get_user_by_login(login: str = Query(...)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, login, first_name, last_name, email
                FROM users
                WHERE login = %s
                """,
                (login,),
            )
            user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return {
        "id": user[0],
        "login": user[1],
        "first_name": user[2],
        "last_name": user[3],
        "email": user[4],
    }

@app.get(
    "/api/v1/users/search",
    response_model=List[UserResponse],
    tags=["Пользователи"],
    summary="Поиск пользователей по имени или фамилии",
)
def search_users(mask: str = Query(...)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, login, first_name, last_name, email
                FROM users
                WHERE LOWER(first_name) LIKE LOWER(%s)
                   OR LOWER(last_name) LIKE LOWER(%s)
                ORDER BY last_name, first_name
                """,
                (f"%{mask}%", f"%{mask}%"),
            )
            rows = cur.fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "id": row[0],
                "login": row[1],
                "first_name": row[2],
                "last_name": row[3],
                "email": row[4],
            }
        )

    return result

#СОБЫТИЯ
@app.post(
    "/api/v1/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["События"],
    summary="Создание события",
)
def create_event(request: EventCreateRequest, current_user: dict = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO events (title, description, event_date, location, organizer_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, title, description, event_date, location, organizer_id
                """,
                (
                    request.title,
                    request.description,
                    request.date,
                    request.location,
                    current_user["id"],
                ),
            )
            event = cur.fetchone()
            conn.commit()

    return {
        "id": event[0],
        "title": event[1],
        "description": event[2],
        "date": str(event[3]),
        "location": event[4],
        "organizer_id": event[5],
    }


@app.get(
    "/api/v1/events",
    response_model=List[EventResponse],
    tags=["События"],
    summary="Получение списка событий",
)
def get_events():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, description, event_date, location, organizer_id
                FROM events
                ORDER BY event_date, id
                """
            )
            rows = cur.fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "date": str(row[3]),
                "location": row[4],
                "organizer_id": row[5],
            }
        )

    return result


@app.get(
    "/api/v1/events/by-date",
    response_model=List[EventResponse],
    tags=["События"],
    summary="Поиск событий по дате",
)
def get_events_by_date(date: str = Query(...)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, description, event_date, location, organizer_id
                FROM events
                WHERE event_date = %s
                ORDER BY id
                """,
                (date,),
            )
            rows = cur.fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "date": str(row[3]),
                "location": row[4],
                "organizer_id": row[5],
            }
        )

    return result


# РЕГИСТРАЦИИ

@app.post(
    "/api/v1/events/{event_id}/registrations",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Регистрации"],
    summary="Регистрация пользователя на событие",
)
def register_for_event(event_id: int, current_user: dict = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM events
                WHERE id = %s
                """,
                (event_id,),
            )
            event = cur.fetchone()

            if not event:
                raise HTTPException(status_code=404, detail="Событие не найдено")

            cur.execute(
                """
                SELECT id
                FROM event_participants
                WHERE event_id = %s
                  AND user_id = %s
                  AND status = 'registered'
                """,
                (event_id, current_user["id"]),
            )
            existing = cur.fetchone()

            if existing:
                raise HTTPException(status_code=409, detail="Пользователь уже зарегистрирован")

            cur.execute(
                """
                INSERT INTO event_participants (event_id, user_id, status)
                VALUES (%s, %s, 'registered')
                RETURNING user_id, event_id, registration_date, status
                """,
                (event_id, current_user["id"]),
            )
            registration = cur.fetchone()
            conn.commit()

    return {
        "user_id": registration[0],
        "event_id": registration[1],
        "registration_date": registration[2].isoformat(),
        "status": registration[3],
    }


@app.get(
    "/api/v1/events/{event_id}/participants",
    response_model=List[UserResponse],
    tags=["Регистрации"],
    summary="Получение участников события",
)
def get_event_participants(event_id: int, current_user: dict = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM events
                WHERE id = %s
                """,
                (event_id,),
            )
            event = cur.fetchone()

            if not event:
                raise HTTPException(status_code=404, detail="Событие не найдено")

            cur.execute(
                """
                SELECT u.id, u.login, u.first_name, u.last_name, u.email
                FROM event_participants ep
                JOIN users u ON u.id = ep.user_id
                WHERE ep.event_id = %s
                  AND ep.status = 'registered'
                ORDER BY u.last_name, u.first_name
                """,
                (event_id,),
            )
            rows = cur.fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "id": row[0],
                "login": row[1],
                "first_name": row[2],
                "last_name": row[3],
                "email": row[4],
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
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.id, e.title, e.description, e.event_date, e.location, e.organizer_id
                FROM event_participants ep
                JOIN events e ON e.id = ep.event_id
                WHERE ep.user_id = %s
                  AND ep.status = 'registered'
                ORDER BY e.event_date, e.id
                """,
                (current_user["id"],),
            )
            rows = cur.fetchall()

    result = []
    for row in rows:
        result.append(
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "date": str(row[3]),
                "location": row[4],
                "organizer_id": row[5],
            }
        )

    return result


@app.delete(
    "/api/v1/events/{event_id}/registrations/me",
    response_model=MessageResponse,
    tags=["Регистрации"],
    summary="Отмена регистрации",
)
def cancel_registration(event_id: int, current_user: dict = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE event_participants
                SET status = 'cancelled'
                WHERE event_id = %s
                  AND user_id = %s
                  AND status = 'registered'
                RETURNING id
                """,
                (event_id, current_user["id"]),
            )
            updated = cur.fetchone()
            conn.commit()

    if not updated:
        raise HTTPException(status_code=404, detail="Регистрация не найдена")

    return {"message": "Регистрация отменена"}