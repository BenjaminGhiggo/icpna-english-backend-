from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.course.entities import Course, CourseClass
from app.domain.course.repository import CourseRepository
from app.infrastructure.database.models import CourseModel, CourseClassModel


class SQLAlchemyCourseRepository(CourseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, course_id: int) -> Optional[Course]:
        result = await self.session.execute(select(CourseModel).where(CourseModel.id == course_id))
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_order(self, order: int) -> Optional[Course]:
        result = await self.session.execute(select(CourseModel).where(CourseModel.order == order))
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_all(self) -> List[Course]:
        result = await self.session.execute(select(CourseModel).order_by(CourseModel.order))
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_by_level(self, level: str) -> List[Course]:
        result = await self.session.execute(
            select(CourseModel).where(CourseModel.level == level).order_by(CourseModel.order)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def create(self, course: Course) -> Course:
        model = CourseModel(
            name=course.name,
            level=course.level,
            book=course.book,
            unit=course.unit,
            cefr_level=course.cefr_level,
            order=course.order,
            description=course.description,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def create_many(self, courses: List[Course]) -> int:
        models = []
        for c in courses:
            models.append(CourseModel(
                name=c.name,
                level=c.level,
                book=c.book,
                unit=c.unit,
                cefr_level=c.cefr_level,
                order=c.order,
                description=c.description,
            ))
        self.session.add_all(models)
        await self.session.commit()
        return len(models)

    async def get_classes(self, course_id: int) -> List[CourseClass]:
        result = await self.session.execute(
            select(CourseClassModel).where(CourseClassModel.course_id == course_id).order_by(CourseClassModel.class_number)
        )
        return [self._class_to_domain(m) for m in result.scalars().all()]

    async def create_class(self, course_class: CourseClass) -> CourseClass:
        model = CourseClassModel(
            course_id=course_class.course_id,
            class_number=course_class.class_number,
            unit_topic=course_class.unit_topic,
            grammar_focus=course_class.grammar_focus,
            vocabulary_focus=course_class.vocabulary_focus,
            skills_focus=course_class.skills_focus,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._class_to_domain(model)

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(CourseModel.id)))
        return result.scalar()

    def _to_domain(self, model: CourseModel) -> Course:
        return Course(
            id=model.id,
            name=model.name,
            level=model.level,
            book=model.book,
            unit=model.unit,
            cefr_level=model.cefr_level,
            order=model.order,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _class_to_domain(self, model: CourseClassModel) -> CourseClass:
        return CourseClass(
            id=model.id,
            course_id=model.course_id,
            class_number=model.class_number,
            unit_topic=model.unit_topic,
            grammar_focus=model.grammar_focus,
            vocabulary_focus=model.vocabulary_focus,
            skills_focus=model.skills_focus,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )