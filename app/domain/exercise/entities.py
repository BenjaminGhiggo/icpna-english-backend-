from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.domain.exercise.value_objects import ExerciseType, DifficultyLevel


@dataclass
class Exercise:
    id: Optional[int] = None
    course_id: int = 0
    class_id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    exercise_type: ExerciseType = ExerciseType.MULTIPLE_CHOICE
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    content: Dict[str, Any] = field(default_factory=dict)
    answers: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls, course_id: int, title: str, exercise_type: ExerciseType,
        content: Dict[str, Any], answers: Dict[str, Any],
        description: Optional[str] = None,
        difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
        class_id: Optional[int] = None,
        created_by: Optional[int] = None,
    ) -> "Exercise":
        return cls(
            course_id=course_id,
            title=title,
            exercise_type=exercise_type,
            content=content,
            answers=answers,
            description=description,
            difficulty=difficulty,
            class_id=class_id,
            created_by=created_by,
        )

    def calculate_score(self, submitted_answers: Dict[str, Any]) -> int:
        if not self.answers:
            return 0
        total = len(self.answers)
        correct = sum(1 for k, v in self.answers.items() if submitted_answers.get(k) == v)
        return int((correct / total) * 100) if total > 0 else 0


@dataclass
class ExerciseAttempt:
    id: Optional[int] = None
    user_id: int = 0
    exercise_id: int = 0
    answers_submitted: Dict[str, Any] = field(default_factory=dict)
    score: int = 0
    time_taken: Optional[int] = None
    is_completed: bool = True
    created_at: Optional[datetime] = None