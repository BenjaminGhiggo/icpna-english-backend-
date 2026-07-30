from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Course:
    id: Optional[int] = None
    name: str = ""
    level: str = "basico"
    book: Optional[str] = None
    unit: Optional[str] = None
    cefr_level: Optional[str] = None
    order: int = 1
    description: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, name: str, level: str, book: str, unit: str, cefr_level: str, order: int) -> "Course":
        return cls(
            name=name,
            level=level,
            book=book,
            unit=unit,
            cefr_level=cefr_level,
            order=order,
        )


@dataclass
class CourseClass:
    id: Optional[int] = None
    course_id: int = 0
    class_number: int = 1
    unit_topic: str = ""
    grammar_focus: Optional[str] = None
    vocabulary_focus: Optional[str] = None
    skills_focus: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None