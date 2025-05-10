from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Family(Base):
    __tablename__ = "families"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    account_number = Column(String, unique=True, nullable=False)
    balance = Column(Numeric(12,2), nullable=False, default=0)

    users = relationship("User", back_populates="family")
    tasks = relationship("Task", back_populates="family")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "parent" или "child"
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)

    family = relationship("Family", back_populates="users")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    deadline = Column(String, nullable=True)
    done_by_child = Column(Boolean, default=False)
    done_by_parent = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)

    family = relationship("Family", back_populates="tasks")
