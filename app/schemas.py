# app/schemas.py
from typing import Optional, List, Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal['parent', 'child']
    parent_family_id: Optional[int]
    parent_email: Optional[EmailStr]

class User(UserBase):
    id: int
    role: str
    family_id: Optional[int]
    created_at: datetime
    child_balance: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class FamilyBase(BaseModel):
    name: Optional[str] = None
    balance: Optional[int] = 0

class FamilyCreate(FamilyBase):
    pass

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
    price: int
    assigned_to_child_id: Optional[int]
    family_id: Optional[int]

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    done_by_parent: Optional[bool]
    is_completed: Optional[bool]
    assigned_to_child_id: Optional[int]
    family_id: Optional[int]

class Task(TaskBase):
    id: int
    price: int
    assigned_to_child_id: Optional[int]
    family_id: Optional[int]
    is_completed: bool
    created_at: datetime

    class Config:
        orm_mode = True

class TopUp(BaseModel):
    amount: int
    class Config:
        schema_extra = {"example": {"amount": 100}}