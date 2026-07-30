from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.exercise.entities import Exercise, ExerciseAttempt
from app.domain.exercise.repository import ExerciseRepository
from app.infrastructure.database.models import ExerciseModel, ExerciseAttemptModel


class SQLAlchemyExerciseRepository(ExerciseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, exercise_id: int) -> Optional[Exercise]:
        result = await self.session.execute(select(ExerciseModel).where(ExerciseModel.id == exercise_id))
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_course(self, course_id: int) -> List[Exercise]:
        result = await self.session.execute(
            select(ExerciseModel).where(ExerciseModel.course_id == course_id, ExerciseModel.is_active == True)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_class(self, class_id: int) -> List[Exercise]:
        result = await self.session.execute(
            select(ExerciseModel).where(ExerciseModel.class_id == class_id, ExerciseModel.is_active == True)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_filters(self, course_id: Optional[int] = None, class_id: Optional[int] = None,
                              exercise_type: Optional[str] = None, difficulty: Optional[str] = None) -> List[Exercise]:
        query = select(ExerciseModel).where(ExerciseModel.is_active == True)
        if course_id:
            query = query.where(ExerciseModel.course_id == course_id)
        if class_id:
            query = query.where(ExerciseModel.class_id == class_id)
        if exercise_type:
            query = query.where(ExerciseModel.exercise_type == exercise_type)
        if difficulty:
            query = query.where(ExerciseModel.difficulty == difficulty)
        result = await self.session.execute(query)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def create(self, exercise: Exercise) -> Exercise:
        model = ExerciseModel(
            course_id=exercise.course_id,
            class_id=exercise.class_id,
            title=exercise.title,
            description=exercise.description,
            exercise_type=exercise.exercise_type.value,
            difficulty=exercise.difficulty.value,
            content=exercise.content,
            answers=exercise.answers,
            created_by=exercise.created_by,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def create_attempt(self, attempt: ExerciseAttempt) -> ExerciseAttempt:
        model = ExerciseAttemptModel(
            user_id=attempt.user_id,
            exercise_id=attempt.exercise_id,
            answers_submitted=attempt.answers_submitted,
            score=attempt.score,
            time_taken=attempt.time_taken,
            is_completed=attempt.is_completed,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._attempt_to_domain(model)

    async def get_attempts(self, user_id: int, exercise_id: int) -> List[ExerciseAttempt]:
        result = await self.session.execute(
            select(ExerciseAttemptModel)
            .where(ExerciseAttemptModel.user_id == user_id, ExerciseAttemptModel.exercise_id == exercise_id)
            .order_by(ExerciseAttemptModel.created_at.desc())
        )
        return [self._attempt_to_domain(m) for m in result.scalars().all()]

    async def get_review_exercises(self, course_id: int) -> List[Exercise]:
        result = await self.session.execute(
            select(ExerciseModel).where(ExerciseModel.course_id == course_id, ExerciseModel.is_active == True)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    def _to_domain(self, model: ExerciseModel) -> Exercise:
        from app.domain.exercise.value_objects import ExerciseType, DifficultyLevel
        return Exercise(
            id=model.id,
            course_id=model.course_id,
            class_id=model.class_id,
            title=model.title,
            description=model.description,
            exercise_type=ExerciseType(model.exercise_type),
            difficulty=DifficultyLevel(model.difficulty),
            content=model.content,
            answers=model.answers,
            is_active=model.is_active,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _attempt_to_domain(self, model: ExerciseAttemptModel) -> ExerciseAttempt:
        return ExerciseAttempt(
            id=model.id,
            user_id=model.user_id,
            exercise_id=model.exercise_id,
            answers_submitted=model.answers_submitted,
            score=model.score,
            time_taken=model.time_taken,
            is_completed=model.is_completed,
            created_at=model.created_at,
        )