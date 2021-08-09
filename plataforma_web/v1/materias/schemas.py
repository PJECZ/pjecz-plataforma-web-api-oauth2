"""
Materias v1.0, esquemas
"""
from pydantic import BaseModel


class MateriaOut(BaseModel):
    """Esquema para entregar materia"""

    id: int
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
