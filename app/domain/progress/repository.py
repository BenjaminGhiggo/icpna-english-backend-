from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.progress.entities import Progress, UserProgress


class ProgressRepository(ABC):
    @abstractmethod
    def get_user_progress(self, user_id: int, course_id: int, class_number: int) -> Optional[Progress]:
        pass

    @abstractmethod
    def list_user_progress(self, user_id: int, course_id: Optional[int] = None) -> List[Progress]:
        pass

    @abstractmethod
    def create_or_update(self, progress: Progress) -> Progress:
        pass

    @abstractmethod
    def update(self, progress_id: int, data: dict) -> Progress:
        pass

    @abstractmethod
    def get_user_summary(self, user_id: int) -> Optional[UserProgress]:
        pass

    @abstractmethod
    def create_or_update_summary(self, summary: UserProgress) -> UserProgress:
        pass

    @abstractmethod
    def get_stats(self, user_id: int) -> dict:
        pass