from fastapi import FastAPI
from app.database import Base, engine
from app.api import users, families, tasks

# Если не используете Alembic, то:
# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(families.router)
app.include_router(tasks.router)
