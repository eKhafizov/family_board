# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(tags=["users"])

@router.post("/register", response_model=schemas.User, status_code=201)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if user_in.role == 'parent':
        # create family automatically
        new_family = models.Family(name=None)
        db.add(new_family)
        db.commit()
        db.refresh(new_family)
        family_id = new_family.id
    else:
        # child must provide parent_family_id or email (crud handles lookup)
        if user_in.parent_family_id:
            family_id = user_in.parent_family_id
        elif user_in.parent_email:
            parent_user = crud.get_user_by_email(db, user_in.parent_email)
            if not parent_user or not parent_user.family_id:
                raise HTTPException(status_code=400, detail="Parent or family not found")
            family_id = parent_user.family_id
        else:
            raise HTTPException(status_code=400, detail="parent_family_id or parent_email required")
    user = crud.create_user(db, user_in, family_id)
    return user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud.authenticate_user(db, form_data)

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(crud.get_current_user)):
    return current_user
