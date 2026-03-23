# Лабораторная работа №2 Лемещенко Мария М8О-107СВ-25

## Разработка REST API сервиса  
Курс: Архитектура программных систем  

## Вариант №22 - Система управления событиями  

В рамках лабораторной работы реализован REST API сервис для управления событиями. Сервис позволяет регистрировать пользователей, создавать события, записываться на них, а также получать информацию об участниках и собственных регистрациях. Реализация выполнена на основе архитектуры, разработанной в лабораторной работе №1, и представляет собой исполняемый вариант внешнего API системы.

## Архитектура решения  

Приложение реализовано как REST API сервис с использованием FastAPI, JWT-аутентификации, Pydantic для валидации данных, in-memory хранилища, а также Docker для контейнеризации.

## Сущности системы  

Пользователь: id, login, first_name, last_name, email, password  
Событие: id, title, description, date, location, organizer_id  
Регистрация: user_id, event_id, registration_date, status  

## Описание API  

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

POST /api/v1/auth/login — получение JWT токена  

Пример запроса:  
{
  "login": "maria",
  "password": "123456"
}

Пример ответа:  
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}

### Пользователи  

GET /api/v1/users/by-login?login=maria — получение пользователя по логину  
GET /api/v1/users/search?mask=mar— поиск пользователей  

### События  

POST /api/v1/events — создание события  

Пример запроса:  
{
  "title": "Конференция",
  "description": "IT мероприятие",
  "date": "2026-05-01",
  "location": "Москва"
}

GET /api/v1/events — получение списка событий  
GET /api/v1/events/by-date?date=2026-05-01 — поиск по дате  

### Регистрации  

POST /api/v1/events/{event_id}/registrations — регистрация на событие  
GET /api/v1/events/{event_id}/participants — получение участников  
GET /api/v1/users/me/events — получение событий пользователя  
DELETE /api/v1/events/{event_id}/registrations/me — отмена регистрации  

## Аутентификация  

Для доступа к защищённым эндпоинтам используется JWT токен.  
Заголовок: Authorization: Bearer <token>  

## Запуск проекта  

Локально:  
pip install -r requirements.txt  
PYTHONPATH=. uvicorn app.main:app --reload  

Документация: http://127.0.0.1:8000/docs  

Docker:  
docker compose build  
docker compose up  

Документация: http://localhost:8000/docs  

## Тестирование  

PYTHONPATH=. pytest  

Все тесты проходят успешно.

## Ограничения  

Используется in-memory хранилище, данные не сохраняются после перезапуска, реализована упрощённая модель безопасности, так как проект учебный.

## Итог  

Реализован полностью рабочий REST API сервис: все эндпоинты реализованны, аутентификация работает, тесты проходят, сервис успешно разворачивается через Docker.
Документация: http://127.0.0.1:8000/docs
Спецификация API представлена в файле openapi.yaml. 