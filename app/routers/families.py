from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.security import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Family])
def list_families(db: Session = Depends(get_db)):
    return db.query(models.Family).all()

@router.post("/", response_model=schemas.Family, status_code=201)
def create_family(fam: schemas.FamilyCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new = models.Family(name=fam.name or "")
    db.add(new); db.commit(); db.refresh(new)
    return new
