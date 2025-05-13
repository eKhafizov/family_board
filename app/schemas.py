from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Базовая схема пользователя
class UserBase(BaseModel):
    email: EmailStr
    full_name: str


# Схема для создания пользователя
class UserCreate(UserBase):
    password: str
    role: Optional[str] = None      # необязательно
    family_id: Optional[int] = None # необязательно
    role: Optional[str] = None      # ← дефолт None
    family_id: Optional[int] = None # ← дефолт None

# Схема для ответа на клиент
class User(UserBase):
    id: int
    role: Optional[str]
    family_id: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}  # Pydantic v2: чтение из ORM-моделей


# Схема для логина
class UserLogin(BaseModel):
    username: EmailStr
    password: str


# JWT-токен
class Token(BaseModel):
    access_token: str
    token_type: str


# Дополнительные данные токена
class TokenData(BaseModel):
    username: Optional[str] = None
