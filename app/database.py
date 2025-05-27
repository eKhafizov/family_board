# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Всегда SQLite в файле test.db рядом с приложением
DATABASE_URL = "sqlite:///./test.db"

# Специальный аргумент для SQLite
connect_args = {"check_same_thread": False}

# Создаём движок и сессию
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

# Генератор сессий для Depends(get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
