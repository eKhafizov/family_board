from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_token



router = APIRouter(prefix="/families", tags=["families"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.FamilyRead)
def create_family(family: schemas.FamilyCreate, db: Session = Depends(get_db)):
    return crud.create_family(db, family)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/{family_id}/top-up", response_model=schemas.FamilyRead)
def top_up(
    family_id: int,
    data: schemas.TopUp,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # только родитель своей семьи
    if current_user.role != "parent" or current_user.family_id != family_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    fam = crud.top_up_family(db, family_id, data.amount)
    if fam is None:
        raise HTTPException(status_code=404, detail="Family not found")
    return fam
