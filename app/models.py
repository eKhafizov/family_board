import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Family(Base):
    __tablename__ = "families"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    members = relationship("User", back_populates="family")
    tasks = relationship("Task", back_populates="family")
    balance = Column(Integer, default=0, nullable=False)  # 💰 баланс семьи


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="parent")
    family_id = Column(Integer, ForeignKey("families.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    family = relationship("Family", back_populates="members")
    tasks = relationship("Task", back_populates="assigned_to")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    done_by_parent = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=True)
    assigned_to_child_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    family = relationship("Family", back_populates="tasks")
    assigned_to = relationship("User", back_populates="tasks")
