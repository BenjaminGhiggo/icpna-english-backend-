from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.progress.entities import Progress, UserProgress
from app.domain.progress.repository import ProgressRepository
from app.infrastructure.database.models import ProgressModel, UserProgressModel


class SQLAlchemyProgressRepository(ProgressRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_progress(self, user_id: int, course_id: int, class_number: int) -> Optional[Progress]:
        result = await self.session.execute(
            select(ProgressModel).where(
                ProgressModel.user_id == user_id,
                ProgressModel.course_id == course_id,
                ProgressModel.class_number == class_number,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_user_progress(self, user_id: int, course_id: Optional[int] = None) -> List[Progress]:
        query = select(ProgressModel).where(ProgressModel.user_id == user_id)
        if course_id:
            query = query.where(ProgressModel.course_id == course_id)
        query = query.order_by(ProgressModel.course_id, ProgressModel.class_number)
        result = await self.session.execute(query)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def create_or_update(self, progress: Progress) -> Progress:
        existing = await self.get_user_progress(progress.user_id, progress.course_id, progress.class_number)
        if existing:
            for key, val in {"status": progress.status, "score": progress.score,
                             "time_spent": progress.time_spent, "notes": progress.notes}.items():
                if val is not None:
                    setattr(existing, key, val if not hasattr(val, 'value') else val.value)
            await self.session.commit()
            return existing
        else:
            model = ProgressModel(
                user_id=progress.user_id,
                course_id=progress.course_id,
                class_number=progress.class_number,
                status=progress.status.value if hasattr(progress.status, 'value') else progress.status,
                score=progress.score,
                time_spent=progress.time_spent,
                notes=progress.notes,
            )
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return self._to_domain(model)

    async def update(self, progress_id: int, data: dict) -> Progress:
        result = await self.session.execute(select(ProgressModel).where(ProgressModel.id == progress_id))
        model = result.scalar_one()
        for key, val in data.items():
            if val is not None and hasattr(model, key):
                setattr(model, key, val)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_user_summary(self, user_id: int) -> Optional[UserProgress]:
        result = await self.session.execute(select(UserProgressModel).where(UserProgressModel.user_id == user_id))
        model = result.scalar_one_or_none()
        return self._summary_to_domain(model) if model else None

    async def create_or_update_summary(self, summary: UserProgress) -> UserProgress:
        result = await self.session.execute(select(UserProgressModel).where(UserProgressModel.user_id == summary.user_id))
        model = result.scalar_one_or_none()
        if model:
            model.current_level = summary.current_level.value
            model.current_course = summary.current_course
            model.overall_score = summary.overall_score
            model.total_time_spent = summary.total_time_spent
            model.courses_completed = summary.courses_completed
            model.exercises_completed = summary.exercises_completed
            model.streak_days = summary.streak_days
            model.last_activity = summary.last_activity
        else:
            model = UserProgressModel(
                user_id=summary.user_id,
                current_level=summary.current_level.value,
                current_course=summary.current_course,
                overall_score=summary.overall_score,
                total_time_spent=summary.total_time_spent,
                courses_completed=summary.courses_completed,
                exercises_completed=summary.exercises_completed,
                streak_days=summary.streak_days,
                last_activity=summary.last_activity,
            )
            self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._summary_to_domain(model)

    async def get_stats(self, user_id: int) -> dict:
        summary = await self.get_user_summary(user_id)
        if not summary:
            return {"total_courses": 33, "completed_courses": 0, "average_score": 0,
                    "total_time_spent": 0, "current_streak": 0}
        return {
            "total_courses": 33,
            "completed_courses": summary.courses_completed,
            "average_score": summary.overall_score,
            "total_time_spent": summary.total_time_spent,
            "current_streak": summary.streak_days,
        }

    def _to_domain(self, model: ProgressModel) -> Progress:
        from app.domain.progress.value_objects import ProgressStatus
        return Progress(
            id=model.id,
            user_id=model.user_id,
            course_id=model.course_id,
            class_number=model.class_number,
            status=ProgressStatus(model.status),
            score=model.score,
            time_spent=model.time_spent,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _summary_to_domain(self, model: UserProgressModel) -> UserProgress:
        from app.domain.progress.value_objects import UserLevel
        return UserProgress(
            id=model.id,
            user_id=model.user_id,
            current_level=UserLevel(model.current_level),
            current_course=model.current_course,
            overall_score=model.overall_score,
            total_time_spent=model.total_time_spent,
            courses_completed=model.courses_completed,
            exercises_completed=model.exercises_completed,
            streak_days=model.streak_days,
            last_activity=model.last_activity,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )