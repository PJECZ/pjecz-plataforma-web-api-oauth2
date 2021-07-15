"""
Materias, esquemas de pydantic
"""
from pydantic import BaseModel


class Materia(BaseModel):
    """Esquema para materias"""

    id: int
    materia: str
