from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import get_db
from app.application.security import get_current_user, get_current_admin_user
from app.domain.user.entities import User
from app.domain.exercise.entities import Exercise, ExerciseAttempt
from app.infrastructure.repositories.exercise_repository import SQLAlchemyExerciseRepository
from app.infrastructure.repositories.course_repository import SQLAlchemyCourseRepository
from app.application.schemas import ExerciseCreate, ExerciseResponse, ExerciseAttemptCreate, ExerciseAttemptResponse

router = APIRouter()


@router.get("/", response_model=List[ExerciseResponse])
async def get_exercises(
    course_id: Optional[int] = None,
    class_id: Optional[int] = None,
    exercise_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyExerciseRepository(db)
    return await repo.list_by_filters(course_id, class_id, exercise_type, difficulty)


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(exercise_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = SQLAlchemyExerciseRepository(db)
    exercise = await repo.get_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return exercise


@router.post("/", response_model=ExerciseResponse)
async def create_exercise(
    exercise_data: ExerciseCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    course_repo = SQLAlchemyCourseRepository(db)
    course = await course_repo.get_by_id(exercise_data.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    repo = SQLAlchemyExerciseRepository(db)
    from app.domain.exercise.value_objects import ExerciseType, DifficultyLevel
    exercise = Exercise.create(
        course_id=exercise_data.course_id,
        title=exercise_data.title,
        exercise_type=ExerciseType(exercise_data.exercise_type),
        content=exercise_data.content,
        answers=exercise_data.answers,
        description=exercise_data.description,
        difficulty=DifficultyLevel(exercise_data.difficulty),
        class_id=exercise_data.class_id,
        created_by=current_admin.id,
    )
    return await repo.create(exercise)


@router.post("/{exercise_id}/attempt", response_model=ExerciseAttemptResponse)
async def submit_exercise_attempt(
    exercise_id: int,
    attempt_data: ExerciseAttemptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyExerciseRepository(db)
    exercise = await repo.get_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    score = exercise.calculate_score(attempt_data.answers_submitted)

    attempt = ExerciseAttempt(
        user_id=current_user.id,
        exercise_id=exercise_id,
        answers_submitted=attempt_data.answers_submitted,
        score=score,
        time_taken=attempt_data.time_taken,
        is_completed=True,
    )
    return await repo.create_attempt(attempt)


@router.get("/{exercise_id}/attempts", response_model=List[ExerciseAttemptResponse])
async def get_exercise_attempts(exercise_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = SQLAlchemyExerciseRepository(db)
    exercise = await repo.get_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return await repo.get_attempts(current_user.id, exercise_id)


@router.get("/review/{course_id}", response_model=List[ExerciseResponse])
async def get_review_exercises(course_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = SQLAlchemyExerciseRepository(db)
    return await repo.get_review_exercises(course_id)