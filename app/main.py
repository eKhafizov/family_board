from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

from app.database import Base, engine
from app.api import users, families, tasks

app = FastAPI()

#  ———————————
# Автоматически создаём все таблицы в БД (SQLite test.db)
try:
    Base.metadata.create_all(bind=engine)
    print("✅ SQLite: tables created (or already existed).")
except Exception as e:
    print("⚠️  Could not create tables:", e)
#  ———————————

app.add_middleware(
    CORSMiddleware,
app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "https://family-board-frontend.onrender.com",

        "https://family-board.onrender.com",

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(families.router, prefix="/families", tags=["families"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])