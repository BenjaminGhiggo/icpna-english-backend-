from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.connection import get_db
from app.application.security import get_current_user, get_current_admin_user
from app.domain.user.entities import User
from app.domain.course.entities import Course
from app.infrastructure.repositories.course_repository import SQLAlchemyCourseRepository
from app.application.schemas import CourseCreate, CourseResponse, CourseClassResponse

router = APIRouter()


@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    level: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = SQLAlchemyCourseRepository(db)
    if level:
        courses = await repo.list_by_level(level)
    else:
        courses = await repo.list_all()
    return courses


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = SQLAlchemyCourseRepository(db)
    course = await repo.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return course


@router.post("/", response_model=CourseResponse)
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    repo = SQLAlchemyCourseRepository(db)
    course = Course.create(
        name=course_data.name,
        level=course_data.level,
        book=course_data.book or "",
        unit=course_data.unit or "",
        cefr_level=course_data.cefr_level or "A1",
        order=course_data.order,
    )
    course.description = course_data.description
    return await repo.create(course)


@router.get("/{course_id}/classes", response_model=List[CourseClassResponse])
async def get_course_classes(course_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = SQLAlchemyCourseRepository(db)
    return await repo.get_classes(course_id)


@router.post("/initialize", response_model=dict)
async def initialize_courses(db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin_user)):
    repo = SQLAlchemyCourseRepository(db)
    existing = await repo.count()
    if existing > 0:
        return {"message": "Cursos ya inicializados", "count": existing}

    courses_data = [
        ("StartUp 1A - Saludos y Presentaciones", "basico", "StartUp 1", "A", "A1", 1),
        ("StartUp 1B - Familia y Hogar", "basico", "StartUp 1", "B", "A1", 2),
        ("StartUp 1C - Comida y Bebida", "basico", "StartUp 1", "C", "A1", 3),
        ("StartUp 1D - Actividades Diarias", "basico", "StartUp 1", "D", "A1", 4),
        ("StartUp 2A - Compras y Numeros", "basico", "StartUp 2", "A", "A2", 5),
        ("StartUp 2B - Salud y Cuerpo", "basico", "StartUp 2", "B", "A2", 6),
        ("StartUp 2C - Viajes y Transporte", "basico", "StartUp 2", "C", "A2", 7),
        ("StartUp 2D - Tiempo Libre", "basico", "StartUp 2", "D", "A2", 8),
        ("StartUp 3A - Experiencias", "basico", "StartUp 3", "A", "A2", 9),
        ("StartUp 3B - Comparaciones", "basico", "StartUp 3", "B", "A2", 10),
        ("StartUp 3C - Fluidez", "basico", "StartUp 3", "C", "A2", 11),
        ("StartUp 3D - Preparacion Intermedio", "basico", "StartUp 3", "D", "A2", 12),
        ("StartUp 4A - Pasado y Narracion", "intermedio", "StartUp 4", "A", "B1", 13),
        ("StartUp 4B - Comunicacion", "intermedio", "StartUp 4", "B", "B1", 14),
        ("StartUp 4C - Opiniones", "intermedio", "StartUp 4", "C", "B1", 15),
        ("StartUp 5A - Noticias y Medios", "intermedio", "StartUp 5", "A", "B1+", 16),
        ("StartUp 5B - Analisis", "intermedio", "StartUp 5", "B", "B1+", 17),
        ("StartUp 5C - Escritura Profesional", "intermedio", "StartUp 5", "C", "B1+", 18),
        ("StartUp 6A - Medios y Periodismo", "intermedio", "StartUp 6", "A", "B2", 19),
        ("StartUp 6B - Psicologia", "intermedio", "StartUp 6", "B", "B2", 20),
        ("StartUp 6C - Fluidez Avanzada", "intermedio", "StartUp 6", "C", "B2", 21),
        ("StartUp 6D - Preparacion Avanzado", "intermedio", "StartUp 6", "D", "B2", 22),
        ("StartUp 6E - Nivelacion", "intermedio", "StartUp 6", "E", "B2", 23),
        ("StartUp 6F - Transicion", "intermedio", "StartUp 6", "F", "B2", 24),
        ("StartUp 7A - Business English", "avanzado", "StartUp 7", "A", "C1", 25),
        ("StartUp 7B - Reportes Profesionales", "avanzado", "StartUp 7", "B", "C1", 26),
        ("StartUp 7C - Comunicacion Efectiva", "avanzado", "StartUp 7", "C", "C1", 27),
        ("StartUp 7D - Analisis Critico", "avanzado", "StartUp 7", "D", "C1", 28),
        ("Project Citizen A", "avanzado", "Project Citizen", "A", "C1", 29),
        ("Project Citizen B", "avanzado", "Project Citizen", "B", "C1", 30),
        ("Project Citizen C", "avanzado", "Project Citizen", "C", "C1", 31),
        ("Project Citizen D", "avanzado", "Project Citizen", "D", "C1", 32),
        ("Project Citizen E", "avanzado", "Project Citizen", "E", "C1", 33),
    ]

    courses = [
        Course.create(name=name, level=level, book=book, unit=unit, cefr_level=cefr, order=order)
        for name, level, book, unit, cefr, order in courses_data
    ]

    count = await repo.create_many(courses)
    return {"message": "Cursos inicializados", "count": count}