from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role            = Column(String, nullable=False)  # "parent" или "child"
    family_id       = Column(Integer, ForeignKey("families.id"))

    family          = relationship("Family", back_populates="members")
    tasks_created   = relationship("Task", back_populates="parent", foreign_keys="Task.parent_id")
    tasks_done      = relationship("Task", back_populates="child",  foreign_keys="Task.child_id")


class Family(Base):
    __tablename__ = "families"
    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String, index=True, nullable=False)
    account_number = Column(String, unique=True, nullable=False)

    members        = relationship("User", back_populates="family")
    tasks          = relationship("Task", back_populates="family")


class Task(Base):
    __tablename__   = "tasks"
    id               = Column(Integer, primary_key=True, index=True)
    description      = Column(String, nullable=False)
    price            = Column(Numeric(10,2), nullable=False)
    deadline         = Column(DateTime, nullable=True)
    done_by_child    = Column(Boolean, default=False)
    done_by_parent   = Column(Boolean, default=False)
    archived         = Column(Boolean, default=False)

    family_id        = Column(Integer, ForeignKey("families.id"))
    parent_id        = Column(Integer, ForeignKey("users.id"))
    child_id         = Column(Integer, ForeignKey("users.id"), nullable=True)

    family           = relationship("Family", back_populates="tasks")
    parent           = relationship("User", back_populates="tasks_created", foreign_keys=[parent_id])
    child            = relationship("User", back_populates="tasks_done",    foreign_keys=[child_id])
