# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from app.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)

# простой get_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/register", response_model=schemas.User, status_code=201)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # проверяем, нет ли уже такого email
    if db.query(models.User).filter_by(email=user_in.email).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")
    # создаём пользователя: full_name = email
    user = models.User(
        email=user_in.email,
        full_name=user_in.email,  # вместо обязательного поля full_name
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)
def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user
