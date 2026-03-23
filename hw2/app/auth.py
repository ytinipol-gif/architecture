from datetime import datetime, timedelta
from fastapi import Header, HTTPException
from typing import Optional
import jwt

from app import storage

SECRET_KEY = "super-puper-secret-key-for-homework-2-event-management-2026"
ALGORITHM = "HS256"


def create_token(user: dict) -> str:
    payload = {
        "sub": str(user["id"]),
        "login": user["login"],
        "exp": datetime.utcnow() + timedelta(hours=24),
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

    user = next((u for u in storage.users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return user