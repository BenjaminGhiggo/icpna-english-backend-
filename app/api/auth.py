from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from app.application.security import verify_password, get_password_hash, create_access_token, get_current_user
from app.infrastructure.database.connection import settings
from app.domain.user.entities import User
from app.application.schemas import UserCreate, UserResponse, Token

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    existing = await repo.get_by_email(user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    user = User.create_student(
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name or user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    created = await repo.create(user)
    return created


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    user = await repo.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/admin/create-admin", response_model=UserResponse)
async def create_admin_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_user),
):
    if not current_admin.is_admin:
        raise HTTPException(status_code=403, detail="Permisos insuficientes")

    repo = SQLAlchemyUserRepository(db)
    existing = await repo.get_by_email(user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    user = User.create_admin(
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name or user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    created = await repo.create(user)
    return created