from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.user.entities import User
from app.domain.user.repository import UserRepository
from app.infrastructure.database.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._to_domain(model)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._to_domain(model)

    async def create(self, user: User) -> User:
        model = UserModel(
            email=user.email or "",
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_student=user.is_student,
            is_admin=user.is_admin,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def list_all(self) -> List[User]:
        result = await self.session.execute(select(UserModel))
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            is_active=model.is_active,
            is_student=model.is_student,
            is_admin=model.is_admin,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )