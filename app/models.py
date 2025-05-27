# app/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Family(Base):
    __tablename__ = 'families'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    balance = Column(Integer, default=0)

    users = relationship('User', back_populates='family')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    family_id = Column(Integer, ForeignKey('families.id'), nullable=True)
    child_balance = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    family = relationship('Family', back_populates='users')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    done_by_parent = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    assigned_to_child_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    family_id = Column(Integer, ForeignKey('families.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Always use SQLite at ./test.db for simplicity
database_file = "./test.db"
DATABASE_URL = f"sqlite:///{database_file}"

# SQLite-specific arg
connect_args = {"check_same_thread": False}

# Engine and session
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
