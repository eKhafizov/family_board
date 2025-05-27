# import os, sys
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.database import engine, Base
# from .routers import users, families, tasks
# from app.routers import users, families, tasks

# app = FastAPI()
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
# print("⚠️ DB schema reset (DEV mode)", file=sys.stderr)

# print("⚠️ Сброс и пересоздание всех таблиц в SQLite (DEV-режим)", file=os.sys.stderr)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(users.router, prefix="/users/users", tags=["users"])
# app.include_router(families.router, prefix="/families", tags=["families"])
# app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import users, families, tasks

# создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS (пример)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры — здесь и задаём один раз префикс
app.include_router(users.router, prefix="/users",   tags=["Users"])
app.include_router(families.router, prefix="/families", tags=["Families"])
app.include_router(tasks.router,    prefix="/tasks",    tags=["Tasks"])
