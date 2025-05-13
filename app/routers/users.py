from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app import models, schemas
from app.database import SessionLocal
from app.security import get_password_hash, verify_password, create_access_token, get_current_user

# Зависимость для доступа к БД

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модель для логина по JSON {username, password}
class LoginData(BaseModel):
    username: EmailStr
    password: str

router = APIRouter()

# Регистрация пользователя
@router.post(
    "/register",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    if db.query(models.User).filter_by(email=user_in.email).first():
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Email already registered",
        )
    user = models.User(
        email=user_in.email,
        full_name=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Логин и получение токена
@router.post(
    "/token",
    response_model=schemas.Token,
)
def login(
    data: LoginData,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter_by(email=data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect email or password",
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Получение информации о текущем пользователе
@router.get(
    "/me",
    response_model=schemas.User,
)
def read_me(
    current_user: models.User = Depends(get_current_user),
):
    return current_user