from datetime import datetime, timedelta
from fastapi import Header, HTTPException
from typing import Optional
import jwt

from app import storage

SECRET_KEY = "super-secret-key-for-hw2-lemeshchenko-maria"
ALGORITHM = "HS256"


def create_token(user: dict) -> str:
    # формирую payload для токена
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

    # поиск пользователя в хранилище
    current_user = None
    for u in storage.users:
        if u["id"] == user_id:
            current_user = u
            break

    if not current_user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    return current_user