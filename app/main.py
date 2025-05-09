from fastapi import FastAPI
from app.api import users, families, tasks

app = FastAPI(title="FamilyBoard API")

app.include_router(users.router)
app.include_router(families.router)
app.include_router(tasks.router)
