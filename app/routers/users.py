 # app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app import models, schemas, security
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_in: schemas.UserCreate = Body(...),
    db: Session = Depends(get_db),
):
    # Проверяем роль
    if user_in.role not in ("parent", "child"):
        raise HTTPException(status_code=400, detail="role must be 'parent' or 'child'")

    # 1) Если родитель — создаём новую семью
    if user_in.role == "parent":
        new_family = models.Family(name="")
        db.add(new_family)
        db.commit()
        db.refresh(new_family)
        family_id = new_family.id

    # 2) Если ребёнок — family_id или parent_email обязательно
    else:
        if not user_in.parent_family_id and not user_in.parent_email:
            raise HTTPException(
                status_code=400,
                detail="Для ребёнка нужно указать parent_family_id или parent_email"
            )
        # по family_id
        if user_in.parent_family_id:
            fam = db.query(models.Family).filter_by(id=user_in.parent_family_id).first()
        else:
            parent = db.query(models.User).filter_by(email=user_in.parent_email, role="parent").first()
            if not parent:
                raise HTTPException(status_code=404, detail="Parent not found")
            fam = db.query(models.Family).filter_by(id=parent.family_id).first()

        if not fam:
            raise HTTPException(status_code=404, detail="Family not found")
        family_id = fam.id

    # 3) Хешируем пароль и создаём пользователя
    hashed_pw = security.get_password_hash(user_in.password)
    new_user = models.User(
        email=user_in.email,
        hashed_password=hashed_pw,
        role=user_in.role,
        family_id=family_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = security.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    return current_user
