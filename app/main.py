# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.database import engine, Base
# from app.routers import users, families, tasks

# app = FastAPI()
# # при старте создаём все таблицы, если ещё нет
# Base.metadata.create_all(bind=engine)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],       # в проде ограничьте до своих доменов
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(users.router, prefix="/users/users", tags=["users"])
# app.include_router(families.router, prefix="/families", tags=["families"])
# app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import users, families, tasks

app = FastAPI()
Base.metadata.create_all(bind=engine)

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
