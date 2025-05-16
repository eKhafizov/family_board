from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi import Body
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.security import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Family])
def list_families(db: Session = Depends(get_db)):
    return db.query(models.Family).all()

@router.post("/", response_model=schemas.Family, status_code=201)
# def create_family(fam: schemas.FamilyCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
#     new = models.Family(name=fam.name or "")
#     db.add(new); db.commit(); db.refresh(new)
#     return new
def create_family(
    fam: schemas.FamilyCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    new_family = models.Family(name=fam.name or "")
    db.add(new_family)
    db.commit()
    db.refresh(new_family)

    # 2) Привязываем текущего пользователя к этой семье
    user.family_id = new_family.id
    db.add(user)
    db.commit()
    db.refresh(user)
    return new_family
    # # 1) создаём новую семью
    # new = models.Family(name=fam.name or "")
    # db.add(new)
    # db.flush()  # привязать new.id без полного коммита

    # # 2) автоматически присваиваем эту семью текущему пользователю
    # user.family_id = new.id
    # db.add(user)

    # # 3) завершаем транзакцию одним коммитом
    # db.commit()
    # db.refresh(new)
    # return new

@router.post(
    "/{family_id}/topup",
    response_model=schemas.Family,
    summary="Пополнить баланс семьи"
)
def top_up_family(
    family_id: int = Path(..., description="ID семьи"),
    data: schemas.TopUp = Body(..., description="Сколько добавить"), 
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    # Только родитель в своей семье может пополнить
    if user.family_id != family_id or user.role != "parent":
        raise HTTPException(403, "Только родитель своей семьи может пополнить баланс")

    fam = db.query(models.Family).filter(models.Family.id == family_id).first()
    if not fam:
        raise HTTPException(404, "Семья не найдена")

    fam.balance += data.amount
    db.commit()
    db.refresh(fam)
    return fam