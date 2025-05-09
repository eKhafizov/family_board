from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import SessionLocal
from app.core.security import verify_token

router = APIRouter(prefix="/tasks", tags=["tasks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return crud.get_user(db, user_id)

@router.get("/", response_model=List[schemas.TaskRead])
def read_tasks(skip: int = 0, limit: int = 100,
               current_user=Depends(get_current_user),
               db: Session = Depends(get_db)):
    return crud.get_tasks(db, current_user.family_id, skip, limit)

@router.post("/", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate,
                current_user=Depends(get_current_user),
                db: Session = Depends(get_db)):
    if current_user.role != "parent":
        raise HTTPException(status_code=403, detail="Only parents can create tasks")
    return crud.create_task(db, task, parent_id=current_user.id, family_id=current_user.family_id)

@router.patch("/{task_id}/done-by-child", response_model=schemas.TaskRead)
def mark_done_by_child(task_id: int,
                       current_user=Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if current_user.role != "child":
        raise HTTPException(status_code=403, detail="Only child can mark done")
    return crud.update_task_status(db, task_id, done_by_child=True)

@router.patch("/{task_id}/done-by-parent", response_model=schemas.TaskRead)
def mark_done_by_parent(task_id: int,
                        current_user=Depends(get_current_user),
                        db: Session = Depends(get_db)):  # ← правильно
    if current_user.role != "parent":
        raise HTTPException(status_code=403, detail="Only parent can confirm task")
    return crud.update_task_status(db, task_id, done_by_parent=True)