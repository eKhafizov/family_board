# app/schemas.py

from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal['parent', 'child']
    # Для ребёнка: укажите либо parent_family_id, либо parent_email
    parent_family_id: Optional[int] = None
    parent_email: Optional[EmailStr] = None

class User(UserBase):
    id: int
    role: Literal['parent', 'child']
    family_id: Optional[int]
    child_balance: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class FamilyBase(BaseModel):
    name: Optional[str] = None
    balance: int = 0

class FamilyCreate(FamilyBase):
    name: Optional[str] = None
    balance: Optional[int] = 0

class Family(FamilyBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    done_by_parent: bool = False

class TaskCreate(TaskBase):
    assigned_to_child_id: Optional[int] = None
    price: int = 0

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done_by_parent: Optional[bool] = None
    is_completed: Optional[bool] = None
    assigned_to_child_id: Optional[int] = None

    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int
    family_id: Optional[int]
    assigned_to_child_id: Optional[int]
    is_completed: bool
    created_at: datetime
    price: int

    class Config:
        orm_mode = True

class TopUp(BaseModel):
    amount: int
    class Config:
        schema_extra = {"example": {"amount": 100}}
