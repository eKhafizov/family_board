from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.security import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Task])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@router.post("/", response_model=schemas.Task, status_code=201)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = models.Task(
        title=data.title,
        description=data.description or "",
        done_by_parent=data.done_by_parent,
        family_id=data.family_id,
        assigned_to_child_id=data.assigned_to_child_id,
    )
    db.add(task); db.commit(); db.refresh(task)
    return task
