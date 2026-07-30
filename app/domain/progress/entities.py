from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.domain.progress.value_objects import ProgressStatus, UserLevel


@dataclass
class Progress:
    id: Optional[int] = None
    user_id: int = 0
    course_id: int = 0
    class_number: int = 1
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    score: Optional[int] = None
    time_spent: Optional[int] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class UserProgress:
    id: Optional[int] = None
    user_id: int = 0
    current_level: UserLevel = UserLevel.BASICO
    current_course: int = 1
    overall_score: int = 0
    total_time_spent: int = 0
    courses_completed: int = 0
    exercises_completed: int = 0
    streak_days: int = 0
    last_activity: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None