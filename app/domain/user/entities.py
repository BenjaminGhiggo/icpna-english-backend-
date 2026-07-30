from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int] = None
    email: Optional[str] = None
    hashed_password: str = ""
    full_name: Optional[str] = None
    is_active: bool = True
    is_student: bool = True
    is_admin: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create_student(cls, email: str, password: str, full_name: str, hashed_password: str) -> "User":
        return cls(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_student=True,
            is_admin=False,
        )

    @classmethod
    def create_admin(cls, email: str, password: str, full_name: str, hashed_password: str) -> "User":
        return cls(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_student=False,
            is_admin=True,
        )