from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.course.entities import Course, CourseClass


class CourseRepository(ABC):
    @abstractmethod
    def get_by_id(self, course_id: int) -> Optional[Course]:
        pass

    @abstractmethod
    def get_by_order(self, order: int) -> Optional[Course]:
        pass

    @abstractmethod
    def list_all(self) -> List[Course]:
        pass

    @abstractmethod
    def list_by_level(self, level: str) -> List[Course]:
        pass

    @abstractmethod
    def create(self, course: Course) -> Course:
        pass

    @abstractmethod
    def create_many(self, courses: List[Course]) -> int:
        pass

    @abstractmethod
    def get_classes(self, course_id: int) -> List[CourseClass]:
        pass

    @abstractmethod
    def create_class(self, course_class: CourseClass) -> CourseClass:
        pass

    @abstractmethod
    def count(self) -> int:
        pass