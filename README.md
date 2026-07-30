# ICPNA English Learning Platform - Backend

Backend para plataforma de aprendizaje de ingles basada en el roadmap del ICPNA (Instituto Cultural Peruano Norteamericano).

## Arquitectura

DDD-Lite (Domain-Driven Design simplificado) con FastAPI + MySQL + Docker.

```
app/
├── domain/                    # Logica de negocio
│   ├── user/                  # Dominio de usuario
│   │   ├── entities.py        # Entidad User
│   │   ├── value_objects.py   # Email, Password, FullName
│   │   └── repository.py     # Interfaz UserRepository
│   ├── course/                # Dominio de cursos
│   │   ├── entities.py        # Entidades Course, CourseClass
│   │   ├── value_objects.py   # CourseLevel, CEFRLevel, CourseOrder
│   │   └── repository.py     # Interfaz CourseRepository
│   ├── exercise/              # Dominio de ejercicios
│   │   ├── entities.py        # Entidades Exercise, ExerciseAttempt
│   │   ├── value_objects.py   # ExerciseType, DifficultyLevel
│   │   └── repository.py     # Interfaz ExerciseRepository
│   └── progress/              # Dominio de progreso
│       ├── entities.py        # Entidades Progress, UserProgress
│       ├── value_objects.py   # ProgressStatus, UserLevel
│       └── repository.py     # Interfaz ProgressRepository
├── infrastructure/            # Implementacion tecnica
│   ├── database/
│   │   ├── connection.py      # Engine, Session, Base, init_db
│   │   ├── base.py            # Base SQLAlchemy
│   │   └── models.py          # Modelos SQLAlchemy (7 tablas)
│   └── repositories/          # Implementaciones de repositorios
│       ├── user_repository.py
│       ├── course_repository.py
│       ├── exercise_repository.py
│       └── progress_repository.py
├── application/               # Capa de aplicacion
│   ├── security.py            # JWT, hashing, dependencias
│   └── schemas.py             # Schemas Pydantic (request/response)
└── api/                       # Endpoints FastAPI
    ├── auth.py                # Autenticacion
    ├── courses.py             # Cursos
    ├── exercises.py           # Ejercicios
    └── progress.py            # Progreso
```

## Tecnologias

- **Framework:** FastAPI 0.115+
- **Base de datos:** MySQL 8.0 (async con aiomysql)
- **ORM:** SQLAlchemy 2.0 (async)
- **Auth:** JWT (python-jose) + bcrypt
- **Validacion:** Pydantic 2.10+
- **Container:** Docker Compose v2
- **Package manager:** uv

## Instalacion

### Requisitos
- Docker y Docker Compose v2
- uv (opcional, para desarrollo local)

### Iniciar con Docker

```bash
cd roadmapenglish/backend
docker compose up -d
```

La API estara disponible en `http://localhost:8000`

### Documentacion automatica

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Desarrollo local (sin Docker)

```bash
cd roadmapenglish/backend
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Requiere MySQL corriendo en `localhost:3307`

## Variables de entorno

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `DATABASE_URL` | `mysql+aiomysql://icpna:icpna123@localhost:3307/icpna_english` | URL de conexion MySQL |
| `SECRET_KEY` | `change-this-in-production` | Clave para JWT |
| `ALGORITHM` | `HS256` | Algoritmo JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Minutos de expiracion del token |

## Base de datos

### Tablas

| Tabla | Descripcion |
|-------|-------------|
| `users` | Usuarios (estudiantes y admin) |
| `courses` | 33 cursos del roadmap ICPNA |
| `course_classes` | Clases por curso (12 por curso) |
| `exercises` | Ejercicios creados por admin |
| `exercise_attempts` | Intentos de ejercicios |
| `progress` | Progreso por clase |
| `user_progress_summary` | Resumen de progreso del usuario |

### Credenciales MySQL

| Campo | Valor |
|-------|-------|
| Host | `localhost:3307` (Docker) / `localhost:3306` (local) |
| Root password | `rootpass` |
| Database | `icpna_english` |
| User | `icpna` |
| Password | `icpna123` |

## API Endpoints

### Autenticacion

| Metodo | Endpoint | Auth | Descripcion |
|--------|----------|------|-------------|
| `POST` | `/api/auth/register` | No | Registrar estudiante |
| `POST` | `/api/auth/login` | No | Login (obtener token) |
| `GET` | `/api/auth/me` | Token | Obtener usuario actual |
| `POST` | `/api/auth/admin/create-admin` | Admin | Crear cuenta admin |

### Cursos

| Metodo | Endpoint | Auth | Descripcion |
|--------|----------|------|-------------|
| `GET` | `/api/courses/` | Token | Listar cursos |
| `GET` | `/api/courses/{id}` | Token | Obtener curso por ID |
| `POST` | `/api/courses/` | Admin | Crear curso |
| `GET` | `/api/courses/{id}/classes` | Token | Listar clases del curso |
| `POST` | `/api/courses/initialize` | Admin | Inicializar 33 cursos ICPNA |

### Ejercicios

| Metodo | Endpoint | Auth | Descripcion |
|--------|----------|------|-------------|
| `GET` | `/api/exercises/` | Token | Listar ejercicios |
| `GET` | `/api/exercises/{id}` | Token | Obtener ejercicio |
| `POST` | `/api/exercises/` | Admin | Crear ejercicio |
| `POST` | `/api/exercises/{id}/attempt` | Token | Responder ejercicio |
| `GET` | `/api/exercises/{id}/attempts` | Token | Ver intentos propios |
| `GET` | `/api/exercises/review/{course_id}` | Token | Ejercicios de repaso |

### Progreso

| Metodo | Endpoint | Auth | Descripcion |
|--------|----------|------|-------------|
| `GET` | `/api/progress/dashboard` | Token | Dashboard del estudiante |
| `GET` | `/api/progress/` | Token | Obtener progreso |
| `POST` | `/api/progress/` | Token | Crear/actualizar progreso |
| `PUT` | `/api/progress/{id}` | Token | Actualizar progreso |
| `GET` | `/api/progress/stats` | Token | Estadisticas |

## Ejemplos curl

### Registrar estudiante

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "maria_8chars.2026@yopmail.com", "password": "test123", "full_name": "Maria Lopez"}'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=maria_8chars.2026@yopmail.com&password=test123"
```

### Obtener usuario actual

```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <token>"
```

### Crear admin (via docker exec)

```bash
docker compose exec app uv run python -c "
from app.infrastructure.database.connection import async_session
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from app.domain.user.entities import User
from app.application.security import get_password_hash
import asyncio
async def create():
    async with async_session() as db:
        repo = SQLAlchemyUserRepository(db)
        await repo.create(User.create_admin(
            'admin_8chars.2026@yopmail.com',
            'admin123',
            'Admin ICPNA',
            get_password_hash('admin123')
        ))
        print('Admin created')
asyncio.run(create())
"
```

### Inicializar cursos

```bash
curl -X POST http://localhost:8000/api/courses/initialize \
  -H "Authorization: Bearer <admin_token>"
```

### Listar cursos

```bash
curl http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer <token>"
```

### Crear ejercicio (admin)

```bash
curl -X POST http://localhost:8000/api/exercises/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Saludos basicos",
    "description": "Prueba tus conocimientos de saludos",
    "exercise_type": "multiple_choice",
    "difficulty": "easy",
    "content": {
      "questions": [
        {
          "id": "q1",
          "text": "Como se dice 'Buenos dias' en ingles?",
          "options": ["Good morning", "Good night", "Goodbye", "Please"]
        }
      ]
    },
    "answers": {"q1": "Good morning"},
    "course_id": 1
  }'
```

### Responder ejercicio

```bash
curl -X POST http://localhost:8000/api/exercises/1/attempt \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"exercise_id": 1, "answers_submitted": {"q1": "Good morning"}, "time_taken": 30}'
```

### Ver ejercicios de repaso

```bash
curl http://localhost:8000/api/exercises/review/1 \
  -H "Authorization: Bearer <token>"
```

### Dashboard

```bash
curl http://localhost:8000/api/progress/dashboard \
  -H "Authorization: Bearer <token>"
```

### Crear progreso

```bash
curl -X POST http://localhost:8000/api/progress/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"course_id": 1, "class_number": 1, "status": "completed", "score": 85, "time_spent": 60}'
```

### Estadisticas

```bash
curl http://localhost:8000/api/progress/stats \
  -H "Authorization: Bearer <token>"
```

## Formato de correos de prueba

Todos los correos de prueba deben seguir el formato:

```
nombre_8chars.2026@yopmail.com
```

Ejemplos:
- `maria_8chars.2026@yopmail.com`
- `pedro_8chars.2026@yopmail.com`
- `admin_8chars.2026@yopmail.com`

## Schemas

### UserCreate
```json
{
  "email": "string",
  "password": "string",
  "full_name": "string (optional)"
}
```

### UserResponse
```json
{
  "id": 0,
  "email": "string",
  "full_name": "string",
  "is_active": true,
  "is_student": true,
  "is_admin": false,
  "created_at": "2026-07-30T00:00:00"
}
```

### CourseCreate
```json
{
  "name": "string",
  "level": "basico|intermedio|avanzado",
  "book": "string (optional)",
  "unit": "string (optional)",
  "cefr_level": "A1|A2|B1|B1+|B2|C1",
  "order": 1,
  "description": "string (optional)"
}
```

### ExerciseCreate
```json
{
  "course_id": 0,
  "class_id": 0,
  "title": "string",
  "description": "string (optional)",
  "exercise_type": "multiple_choice|fill_blank|matching|true_false|writing",
  "difficulty": "easy|medium|hard",
  "content": {},
  "answers": {}
}
```

### ProgressCreate
```json
{
  "course_id": 0,
  "class_number": 1,
  "status": "not_started|in_progress|completed",
  "score": 0,
  "time_spent": 0,
  "notes": "string"
}
```

## Roadmap ICPNA

El documento `ROADMAP-ICPNA.md` (en la raiz del proyecto) contiene:

- Estructura completa del programa (33 cursos, 396 clases)
- Vocabulario por categorias
- Lista de verbos y tiempos verbales
- Phrasal verbs por nivel
- Mapeo CEFR
- Sistema de evaluacion

## Desarrollo

### Agregar nuevo dominio

1. Crear carpeta en `app/domain/nuevo_dominio/`
2. Definir entidades en `entities.py`
3. Definir value objects en `value_objects.py`
4. Definir interfaz del repositorio en `repository.py`
5. Crear modelo SQLAlchemy en `app/infrastructure/database/models.py`
6. Implementar repositorio en `app/infrastructure/repositories/`
7. Crear schemas en `app/application/schemas.py`
8. Crear router en `app/api/`
9. Registrar router en `app/main.py`

### Ejecutar tests

```bash
docker compose exec app uv run pytest
```

### Ver logs

```bash
docker compose logs -f app
docker compose logs -f mysql
```

### Detener servicios

```bash
docker compose down
```

### Detener y eliminar datos

```bash
docker compose down -v
```