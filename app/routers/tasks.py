from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.security import get_db, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Path, Body

router = APIRouter()

@router.get("/", response_model=List[schemas.Task])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@router.put(
    "/{task_id}",
    response_model=schemas.Task,
    summary="Обновить задачу частично или полностью"
)
def update_task(
    task_id: int = Path(..., description="ID задачи"),
    data: schemas.TaskUpdate = Body(..., description="Поля для обновления"),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

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
