# Лабораторная работа №2  
Лемещенко Мария М8О-107СВ-25  

## Тема  
Разработка REST API сервиса  
Курс: Программная инженерия

## Вариант №22 — Система управления событиями  

В рамках данной лабораторной работы я реализовала REST API сервис для управления событиями. Сервис позволяет регистрировать пользователей, создавать события, записываться на них и просматривать информацию об участниках. Проект является продолжением первой лабораторной работы и представляет собой уже работающий API.

## Что используется  

FastAPI, JWT-аутентификация, Pydantic для валидации данных, in-memory хранилище, Docker.

## Структура данных  

Пользователь: id, login, first_name, last_name, email, password  
Событие: id, title, description, date, location, organizer_id  
Регистрация: user_id, event_id, registration_date, status  

## Основные эндпоинты  

### Аутентификация  

POST /api/v1/auth/register — регистрация пользователя  

Пример запроса:
{
  "login": "maria",
  "first_name": "Maria",
  "last_name": "Lemeshchenko",
  "email": "maria@gmail.com",
  "password": "123456"
}

POST /api/v1/auth/login — вход и получение токена  

Пример запроса:
{
  "login": "maria",
  "password": "123456"
}

Пример ответа:
{
  "access_token": "...",
  "token_type": "bearer"
}

### Пользователи  

GET /api/v1/users/by-login?login=maria - получить пользователя  
GET /api/v1/users/search?mask=mar - поиск по имени или фамилии  

### События  

POST /api/v1/events — создание события  

Пример запроса:
{
  "title": "Митап",
  "description": "Обсуждение архитектуры",
  "date": "2026-05-01",
  "location": "Москва"
}

GET /api/v1/events — список событий  
GET /api/v1/events/by-date?date=2026-05-01 — поиск по дате  

### Регистрации  

POST /api/v1/events/{event_id}/registrations — регистрация на событие  
GET /api/v1/events/{event_id}/participants — получение участников  
GET /api/v1/users/me/events — мои события  
DELETE /api/v1/events/{event_id}/registrations/me — отмена регистрации  

## Аутентификация  

Для защищённых запросов используется JWT токен.  
Заголовок: Authorization: Bearer <token>  

## Как запустить  

Локально:
pip install -r requirements.txt  
PYTHONPATH=. uvicorn app.main:app --reload  

Документация:
http://127.0.0.1:8000/docs  

Через Docker:
docker compose build  
docker compose up  

Документация:
http://localhost:8000/docs  

## Тестирование  

PYTHONPATH=. pytest  

Все тесты проходят успешно.

## Ограничения  

Данные хранятся в памяти, поэтому при перезапуске приложения они теряются. 

## Итог  

В ходе работы был реализован рабочий REST API сервис с базовой логикой: регистрация пользователей, создание событий и работа с регистрациями. Сервис можно запускать локально и через Docker, все основные сценарии покрыты тестами.