from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, condecimal

# --- Task ---
class TaskBase(BaseModel):
    description: str
    price: condecimal(max_digits=10, decimal_places=2)
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    child_id: Optional[int] = None

class TaskRead(TaskBase):
    id: int
    done_by_child: bool
    done_by_parent: bool
    archived: bool
    parent_id: int
    family_id: int
    child_id: Optional[int]

    class Config:
        from_attributes = True

# --- User ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str               # "parent" или "child"
    family_id: Optional[int]

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    family_id: Optional[int]

    class Config:
        from_attributes = True

# --- Family ---
class FamilyCreate(BaseModel):
    name: str
    account_number: str

class FamilyRead(BaseModel):
    id: int
    name: str
    account_number: str

    class Config:
        from_attributes = True

# --- JWT ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None



class TopUp(BaseModel):
    amount: condecimal(max_digits=12, decimal_places=2)
