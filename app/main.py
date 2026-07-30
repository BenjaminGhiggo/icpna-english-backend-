from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import auth, courses, exercises, progress
from app.infrastructure.database.connection import init_db, async_session
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from app.application.security import get_password_hash
from app.domain.user.entities import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with async_session() as session:
        repo = SQLAlchemyUserRepository(session)
        existing = await repo.get_by_email("admin@icpna.edu.pe")
        if not existing:
            admin = User.create_admin(
                email="admin@icpna.edu.pe",
                password="admin123",
                full_name="Admin ICPNA",
                hashed_password=get_password_hash("admin123"),
            )
            await repo.create(admin)
    yield


app = FastAPI(
    title="ICPNA English Learning Platform",
    description="Backend DDD-Lite con FastAPI + PostgreSQL",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(courses.router, prefix="/api/courses", tags=["courses"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])


@app.get("/")
async def root():
    return {"message": "ICPNA English Learning Platform API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}