from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Header, HTTPException

from app.database import get_database

SECRET_KEY = "super-secret-key-for-hw4-lemeshchenko-maria"
ALGORITHM = "HS256"


def create_token(user: dict) -> str:
    payload = {
        "sub": str(user["id"]),
        "login": user["login"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: Optional[str] = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Отсутствует или неверный токен")

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Неверный токен")

    user = get_database().users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return user
