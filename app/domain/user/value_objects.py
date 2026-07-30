from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.value):
            raise ValueError(f"Email inválido: {self.value}")


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        if len(self.value) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")


@dataclass(frozen=True)
class FullName:
    value: str

    def __post_init__(self):
        if len(self.value.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")