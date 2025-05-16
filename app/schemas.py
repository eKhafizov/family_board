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
    child_balance: int

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
    balance: Optional[int] = 0

class FamilyCreate(FamilyBase):
    # pass
    name: Optional[str]
    balance: Optional[int] = 0

class Family(FamilyBase):
    id: int
    created_at: datetime
    balance: int
    

    class Config:
        orm_mode = True

# ——— Task ————————————————————————————————————————
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    done_by_parent: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done_by_parent: Optional[bool] = None
    is_completed: Optional[bool] = None
    family_id: Optional[int] = None
    assigned_to_child_id: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class TaskCreate(TaskBase):
    assigned_to_child_id: Optional[int] = None
    family_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    price: int

class Task(TaskBase):
    id: int
    family_id: Optional[int]
    assigned_to_child_id: Optional[int]
    is_completed: bool
    created_at: datetime
    price: int # добавил 

    class Config:
        orm_mode = True


class TopUp(BaseModel):
    amount: int  # сколько добавить

    class Config:
        schema_extra = {
            "example": {"amount": 100}
        }