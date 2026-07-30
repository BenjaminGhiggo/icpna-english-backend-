from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


# Auth
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    is_student: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


# Course
class CourseCreate(BaseModel):
    name: str
    level: str
    book: Optional[str] = None
    unit: Optional[str] = None
    cefr_level: Optional[str] = None
    order: int
    description: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    name: str
    level: str
    book: Optional[str]
    unit: Optional[str]
    cefr_level: Optional[str]
    order: int
    description: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class CourseClassResponse(BaseModel):
    id: int
    course_id: int
    class_number: int
    unit_topic: str
    grammar_focus: Optional[str]
    vocabulary_focus: Optional[str]
    skills_focus: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Exercise
class ExerciseCreate(BaseModel):
    course_id: int
    class_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    exercise_type: str
    difficulty: str = "medium"
    content: Dict[str, Any]
    answers: Dict[str, Any]

class ExerciseResponse(BaseModel):
    id: int
    course_id: int
    class_id: Optional[int]
    title: str
    description: Optional[str]
    exercise_type: str
    difficulty: str
    content: Dict[str, Any]
    answers: Dict[str, Any]
    is_active: bool
    created_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class ExerciseAttemptCreate(BaseModel):
    exercise_id: int
    answers_submitted: Dict[str, Any]
    time_taken: Optional[int] = None

class ExerciseAttemptResponse(BaseModel):
    id: int
    user_id: int
    exercise_id: int
    answers_submitted: Dict[str, Any]
    score: int
    time_taken: Optional[int]
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Progress
class ProgressCreate(BaseModel):
    course_id: int
    class_number: int
    status: str = "not_started"
    score: Optional[int] = None
    time_spent: Optional[int] = None
    notes: Optional[str] = None

class ProgressUpdate(BaseModel):
    status: Optional[str] = None
    score: Optional[int] = None
    time_spent: Optional[int] = None
    notes: Optional[str] = None

class ProgressResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    class_number: int
    status: str
    score: Optional[int]
    time_spent: Optional[int]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    current_level: str
    current_course: int
    overall_score: int
    total_time_spent: int
    courses_completed: int
    exercises_completed: int
    streak_days: int
    last_activity: Optional[datetime]
    recent_activity: List[Dict[str, Any]] = []
    upcoming_classes: List[Dict[str, Any]] = []