from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.core.security import get_password_hash, create_access_token
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=schemas.User, status_code=201)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    role = user_in.role or "parent"       # пример: первый юзер — родитель
    family_id = user_in.family_id or None # или сразу создаёте новую семью

    user = models.User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=pwd_context.hash(user_in.password),
        role=role,
        family_id=family_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
# @router.post("/register", response_model=schemas.UserRead)
# def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
#     if crud.get_user_by_email(db, user_in.email):
#         raise HTTPException(status_code=400, detail="Email already registered")
#     if not crud.get_family(db, user_in.family_id):
#         raise HTTPException(status_code=400, detail="Family not found")
#     hashed = get_password_hash(user_in.password)
#     user = crud.create_user(db, user_in, hashed)
#     return user

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserRead)
def read_me(current_user=Depends(get_current_user)):
    return current_user
