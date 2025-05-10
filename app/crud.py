from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models, schemas
from decimal import Decimal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Users ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed,
        role=user.role,
        family_id=user.family_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

# --- Families ---
def create_family(db: Session, family: schemas.FamilyCreate):
    db_family = models.Family(
        name=family.name,
        account_number=family.account_number,
    )
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family

# --- Tasks ---
def get_tasks(db: Session, family_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Task)
        .filter(models.Task.family_id == family_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_task(db: Session, task: schemas.TaskCreate, parent_id: int, family_id: int):
    db_task = models.Task(
        **task.dict(),
        parent_id=parent_id,
        family_id=family_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task_status(db: Session, task_id: int, done_by_child: bool = None, done_by_parent: bool = None):
    db_task = db.query(models.Task).get(task_id)
    if done_by_child is not None:
        db_task.done_by_child = done_by_child
    if done_by_parent is not None:
        db_task.done_by_parent = done_by_parent
        if done_by_parent:
            db_task.archived = True
            # TODO: финансовые операции
    db.commit()
    db.refresh(db_task)
    return db_task



def top_up_family(db: Session, family_id: int, amount: Decimal):
    """Увеличить balance указанной семьи на amount."""
    fam = db.query(models.Family).get(family_id)
    if not fam:
        return None
    fam.balance += amount
    db.commit()
    db.refresh(fam)
    return fam
