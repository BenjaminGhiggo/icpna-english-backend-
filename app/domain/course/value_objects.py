from dataclasses import dataclass
from enum import Enum


class CourseLevel(str, Enum):
    BASICO = "basico"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"


@dataclass(frozen=True)
class CEFRLevel:
    value: str

    def __post_init__(self):
        valid = ["A1", "A2", "B1", "B1+", "B2", "C1"]
        if self.value not in valid:
            raise ValueError(f"Nivel CEFR inválido: {self.value}. Válidos: {valid}")


@dataclass(frozen=True)
class CourseOrder:
    value: int

    def __post_init__(self):
        if not 1 <= self.value <= 33:
            raise ValueError(f"Orden debe ser 1-33, recibido: {self.value}")