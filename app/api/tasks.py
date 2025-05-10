# app/api/tasks.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskRead)
def create_task(
    task_in: schemas.TaskCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "parent":
        raise HTTPException(status_code=403, detail="Only parents can create tasks")
    task = crud.create_task(db, current_user.family_id, task_in)
    return task

@router.get("/", response_model=List[schemas.TaskRead])
def list_tasks(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_tasks_for_family(db, current_user.family_id)

@router.post("/{task_id}/done_by_child", response_model=schemas.TaskRead)
def mark_done_by_child(
    task_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "child":
        raise HTTPException(status_code=403, detail="Only child can mark tasks done")
    task = crud.mark_done_child(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/{task_id}/done_by_parent", response_model=schemas.TaskRead)
def mark_done_by_parent(
    task_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "parent":
        raise HTTPException(status_code=403, detail="Only parent can confirm tasks")
    task = crud.mark_done_parent(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not done by child")
    return task
