from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_student = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    progress = relationship("ProgressModel", back_populates="user")
    exercise_attempts = relationship("ExerciseAttemptModel", back_populates="user")


class CourseModel(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    level = Column(String(50), nullable=False)
    book = Column(String(100))
    unit = Column(String(10))
    cefr_level = Column(String(10))
    order = Column(Integer, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    classes = relationship("CourseClassModel", back_populates="course")
    exercises = relationship("ExerciseModel", back_populates="course")


class CourseClassModel(Base):
    __tablename__ = "course_classes"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    class_number = Column(Integer, nullable=False)
    unit_topic = Column(String(255), nullable=False)
    grammar_focus = Column(Text)
    vocabulary_focus = Column(Text)
    skills_focus = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    course = relationship("CourseModel", back_populates="classes")
    exercises = relationship("ExerciseModel", back_populates="course_class")


class ExerciseModel(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("course_classes.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    exercise_type = Column(String(50), nullable=False)
    difficulty = Column(String(20), default="medium")
    content = Column(JSON, nullable=False)
    answers = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    course = relationship("CourseModel", back_populates="exercises")
    course_class = relationship("CourseClassModel", back_populates="exercises")
    attempts = relationship("ExerciseAttemptModel", back_populates="exercise")


class ExerciseAttemptModel(Base):
    __tablename__ = "exercise_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    answers_submitted = Column(JSON, nullable=False)
    score = Column(Integer, nullable=False)
    time_taken = Column(Integer)
    is_completed = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserModel", back_populates="exercise_attempts")
    exercise = relationship("ExerciseModel", back_populates="attempts")


class ProgressModel(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    class_number = Column(Integer, nullable=False)
    status = Column(String(20), default="not_started")
    score = Column(Integer)
    time_spent = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("UserModel", back_populates="progress")
    course = relationship("CourseModel")


class UserProgressModel(Base):
    __tablename__ = "user_progress_summary"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_level = Column(String(20), default="basico")
    current_course = Column(Integer, default=1)
    overall_score = Column(Integer, default=0)
    total_time_spent = Column(Integer, default=0)
    courses_completed = Column(Integer, default=0)
    exercises_completed = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_activity = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("UserModel")