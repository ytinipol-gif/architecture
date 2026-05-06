from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    login: str = Field(..., description="логин")
    first_name: str = Field(..., description="имя")
    last_name: str = Field(..., description="фамилия")
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLoginRequest(BaseModel):
    login: str
    password: str


class UserResponse(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class EventCreateRequest(BaseModel):
    title: str
    description: str
    date: str
    location: str


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

