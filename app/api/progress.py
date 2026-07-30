from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.infrastructure.database.connection import get_db
from app.application.security import get_current_user
from app.domain.user.entities import User
from app.domain.progress.entities import Progress, UserProgress
from app.infrastructure.repositories.progress_repository import SQLAlchemyProgressRepository
from app.infrastructure.repositories.course_repository import SQLAlchemyCourseRepository
from app.application.schemas import ProgressCreate, ProgressUpdate, ProgressResponse, DashboardResponse

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = SQLAlchemyProgressRepository(db)
    course_repo = SQLAlchemyCourseRepository(db)

    summary = await repo.get_user_summary(current_user.id)
    if not summary:
        summary = UserProgress(user_id=current_user.id, last_activity=datetime.utcnow())
        summary = await repo.create_or_update_summary(summary)

    recent_progress = await repo.list_user_progress(current_user.id)
    recent_activity = []
    for p in recent_progress[-5:]:
        course = await course_repo.get_by_id(p.course_id)
        if course:
            recent_activity.append({
                "course_name": course.name,
                "class_number": p.class_number,
                "status": p.status.value if hasattr(p.status, 'value') else p.status,
                "score": p.score,
                "updated_at": p.updated_at.isoformat() if p.updated_at else None,
            })

    upcoming = []
    current_course = await course_repo.get_by_order(summary.current_course)
    if current_course:
        classes = await course_repo.get_classes(current_course.id)
        for c in classes[:3]:
            upcoming.append({
                "course_name": current_course.name,
                "class_number": c.class_number,
                "unit_topic": c.unit_topic,
            })

    return DashboardResponse(
        current_level=summary.current_level.value,
        current_course=summary.current_course,
        overall_score=summary.overall_score,
        total_time_spent=summary.total_time_spent,
        courses_completed=summary.courses_completed,
        exercises_completed=summary.exercises_completed,
        streak_days=summary.streak_days,
        last_activity=summary.last_activity,
        recent_activity=recent_activity,
        upcoming_classes=upcoming,
    )


@router.get("/", response_model=List[ProgressResponse])
async def get_user_progress(
    course_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyProgressRepository(db)
    return await repo.list_user_progress(current_user.id, course_id)


@router.post("/", response_model=ProgressResponse)
async def create_or_update_progress(
    progress_data: ProgressCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyProgressRepository(db)
    from app.domain.progress.value_objects import ProgressStatus
    progress = Progress(
        user_id=current_user.id,
        course_id=progress_data.course_id,
        class_number=progress_data.class_number,
        status=ProgressStatus(progress_data.status),
        score=progress_data.score,
        time_spent=progress_data.time_spent,
        notes=progress_data.notes,
    )
    return await repo.create_or_update(progress)


@router.put("/{progress_id}", response_model=ProgressResponse)
async def update_progress(
    progress_id: int,
    progress_update: ProgressUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyProgressRepository(db)
    data = {k: v for k, v in progress_update.model_dump().items() if v is not None}
    return await repo.update(progress_id, data)


@router.get("/stats", response_model=dict)
async def get_progress_stats(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = SQLAlchemyProgressRepository(db)
    return await repo.get_stats(current_user.id)