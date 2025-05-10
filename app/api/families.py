from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/families", tags=["families"])

@router.post("/", response_model=schemas.FamilyRead)
def create_family(
    family_in: schemas.FamilyCreate,
    db: Session = Depends(get_db),
):
    return crud.create_family(db, family_in)

@router.post("/{family_id}/top-up", response_model=schemas.FamilyRead)
def top_up_family(
    family_id: int,
    data: schemas.TopUp,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "parent" or current_user.family_id != family_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    fam = crud.top_up_family(db, family_id, data.amount)
    if not fam:
        raise HTTPException(status_code=404, detail="Family not found")
    return fam
