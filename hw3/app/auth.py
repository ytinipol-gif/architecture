from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Header, HTTPException

from app.db import get_connection

SECRET_KEY = "super-secret-key-for-hw2-lemeshchenko-maria"
ALGORITHM = "HS256"


def create_token(user: dict) -> str:
    payload = {}
    payload["sub"] = str(user["id"])
    payload["login"] = user["login"]
    payload["exp"] = datetime.utcnow() + timedelta(hours=24)

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(authorization: Optional[str] = Header(default=None)) -> dict:
    # проверяю наличие токена в заголовке
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Отсутствует или неверный токен")

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Неверный токен")
# поиск пользователя в базе данных
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, login, first_name, last_name, email
                FROM users
                WHERE id = %s
                """,
                (user_id,),
            )
            user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return {
        "id": user[0],
        "login": user[1],
        "first_name": user[2],
        "last_name": user[3],
        "email": user[4],
    }
