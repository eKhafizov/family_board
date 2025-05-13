from pydantic import BaseModel, EmailStr, condecimal
from decimal import Decimal
from typing import Optional, List

# --- Users ---
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Optional[str] = None      # теперь не обязателен
    family_id: Optional[int] = None # теперь не обязателен

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    family_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Families ---
class FamilyCreate(BaseModel):
    name: str
    account_number: str

class FamilyRead(BaseModel):
    id: int
    name: str
    account_number: str
    balance: Decimal

    class Config:
        from_attributes = True

class TopUp(BaseModel):
    amount: condecimal(max_digits=12, decimal_places=2)

# --- Tasks ---
class TaskCreate(BaseModel):
    task: str
    price: condecimal(max_digits=10, decimal_places=2)
    deadline: Optional[str]

class TaskRead(BaseModel):
    id: int
    task: str
    price: Decimal
    deadline: Optional[str]
    done_by_child: bool
    done_by_parent: bool
    archived: bool

    class Config:
        from_attributes = True
