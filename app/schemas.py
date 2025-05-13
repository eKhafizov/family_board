# app/schemas.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

# ——— User —————————————————————————————————————————
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    role: str
    family_id: Optional[int]
    created_at: datetime
    class Config:
        orm_mode = True

# ——— Token ————————————————————————————————————————
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ——— Family и Task (без изменений) ————————————————————————
# … ваши схемы для FamilyCreate, Family, TaskCreate, Task …
