from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.exercise.entities import Exercise, ExerciseAttempt


class ExerciseRepository(ABC):
    @abstractmethod
    def get_by_id(self, exercise_id: int) -> Optional[Exercise]:
        pass

    @abstractmethod
    def list_by_course(self, course_id: int) -> List[Exercise]:
        pass

    @abstractmethod
    def list_by_class(self, class_id: int) -> List[Exercise]:
        pass

    @abstractmethod
    def list_by_filters(self, course_id: Optional[int] = None, class_id: Optional[int] = None,
                        exercise_type: Optional[str] = None, difficulty: Optional[str] = None) -> List[Exercise]:
        pass

    @abstractmethod
    def create(self, exercise: Exercise) -> Exercise:
        pass

    @abstractmethod
    def create_attempt(self, attempt: ExerciseAttempt) -> ExerciseAttempt:
        pass

    @abstractmethod
    def get_attempts(self, user_id: int, exercise_id: int) -> List[ExerciseAttempt]:
        pass

    @abstractmethod
    def get_review_exercises(self, course_id: int) -> List[Exercise]:
        pass