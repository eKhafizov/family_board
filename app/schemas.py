from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

# ——— User —————————————————————————————————————————
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
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

# ——— Family ——————————————————————————————————————
class FamilyBase(BaseModel):
    name: Optional[str] = None

class FamilyCreate(FamilyBase):
    pass

class Family(FamilyBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# ——— Task ————————————————————————————————————————
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    done_by_parent: bool = False

class TaskCreate(TaskBase):
    assigned_to_child_id: Optional[int] = None
    family_id: Optional[int] = None

class Task(TaskBase):
    id: int
    family_id: Optional[int]
    assigned_to_child_id: Optional[int]
    is_completed: bool
    created_at: datetime
    class Config:
        orm_mode = True
