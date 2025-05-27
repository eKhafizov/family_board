# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Проверяем доступность драйвера PostgreSQL
try:
    import psycopg2  # noqa: F401
    _has_psycopg2 = True
except ImportError:
    _has_psycopg2 = False

# Если задана внешняя БД и драйвер доступен, используем её, иначе всегда SQLite
env_db = os.getenv("DATABASE_URL")
if env_db and _has_psycopg2:
    DATABASE_URL = env_db
else:
    DATABASE_URL = "sqlite:///./test.db"

# Аргументы для SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Создаём движок
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# Сессии
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Базовый класс
Base = declarative_base()

# Зависимость для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
