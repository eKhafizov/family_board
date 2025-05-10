from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import verify_password

def create_family(db: Session, family_in: schemas.FamilyCreate):
    fam = models.Family(
        name=family_in.name,
        account_number=family_in.account_number,
        balance=Decimal("0.00")
    )
    db.add(fam)
    try:
        db.commit()
        db.refresh(fam)
        return fam
    except IntegrityError as e:
        db.rollback()
        if "account_number" in str(e.orig).lower():
            raise HTTPException(status_code=400, detail="Account number already registered")
        raise

def get_family(db: Session, family_id: int):
    return db.query(models.Family).get(family_id)

def get_user(db: Session, user_id: int):
    return db.query(models.User).get(user_id)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_in: schemas.UserCreate, hashed_password: str):
    user = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role,
        family_id=user_in.family_id
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        msg = str(e.orig).lower()
        if "unique constraint" in msg or "users_email_key" in msg:
            raise HTTPException(status_code=400, detail="Email already registered")
        if "foreign key constraint" in msg:
            raise HTTPException(status_code=400, detail="Family not found")
        raise

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def top_up_family(db: Session, family_id: int, amount: Decimal):
    fam = db.query(models.Family).get(family_id)
    if not fam:
        return None
    fam.balance += amount
    db.commit()
    db.refresh(fam)
    return fam

def create_task(db: Session, family_id: int, task_in: schemas.TaskCreate):
    task = models.Task(
        task=task_in.task,
        price=task_in.price,
        deadline=task_in.deadline,
        family_id=family_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks_for_family(db: Session, family_id: int):
    return db.query(models.Task).filter(models.Task.family_id==family_id, models.Task.archived==False).all()

def mark_done_child(db: Session, task_id: int):
    task = db.query(models.Task).get(task_id)
    if not task:
        return None
    task.done_by_child = True
    db.commit()
    db.refresh(task)
    return task

def mark_done_parent(db: Session, task_id: int):
    task = db.query(models.Task).get(task_id)
    if not task or not task.done_by_child:
        return None
    task.done_by_parent = True
    task.archived = True
    db.commit()
    db.refresh(task)
    return task
