import os, sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from .routers import users, families, tasks
from app.routers import users, families, tasks

app = FastAPI()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("⚠️ DB schema reset (DEV mode)", file=sys.stderr)

print("⚠️ Сброс и пересоздание всех таблиц в SQLite (DEV-режим)", file=os.sys.stderr)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users/users", tags=["users"])
app.include_router(families.router, prefix="/families", tags=["families"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
