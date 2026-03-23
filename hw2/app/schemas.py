from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    login: str = Field(..., examples=["maria"], description="Логин пользователя")
    first_name: str = Field(..., examples=["Мария"], description="Имя пользователя")
    last_name: str = Field(..., examples=["Лемещенко"], description="Фамилия пользователя")
    email: EmailStr = Field(..., examples=["maria@gmail.com"], description="Email пользователя")
    password: str = Field(..., min_length=6, examples=["123456"], description="Пароль")


class UserLoginRequest(BaseModel):
    login: str = Field(..., examples=["maria"], description="Логин")
    password: str = Field(..., examples=["123456"], description="Пароль")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
    email: EmailStr


class EventCreateRequest(BaseModel):
    title: str = Field(..., examples=["Архитектурный митап"], description="Название события")
    description: str = Field(..., examples=["Обсуждение архитектуры"], description="Описание события")
    date: str = Field(..., examples=["2026-03-25"], description="Дата события")
    location: str = Field(..., examples=["Москва"], description="Место проведения")


class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    date: str
    location: str
    organizer_id: int


class RegistrationResponse(BaseModel):
    user_id: int
    event_id: int
    registration_date: str
    status: str


class MessageResponse(BaseModel):
    message: str