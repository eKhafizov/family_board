import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1) Переходим на SQLite по умолчанию (если не задано DATABASE_URL),
#    или берём внешнюю БД, если переменная окружения прописана.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"  # файл test.db в корне проекта
)

# Для SQLite нужен специальный аргумент:
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# создаём двигатель (engine) с пулом и проверкой соединения
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# создаём Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# базовый класс для моделей
Base = declarative_base()

# 2) Функция-генератор для Depends(get_db) в FastAPI

def get_db():
    """
    Возвращает сессию базы данных для каждого запроса и закрывает её по завершении.
    Использовать в маршрутах FastAPI:
        def endpoint(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
