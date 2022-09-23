"""
Materias v1.0, esquemas
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class MateriaOut(BaseModel):
    """Esquema para entregar materia"""

    id: int | None
    nombre: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneMateriaOut(MateriaOut, OneBaseOut):
    """Esquema para entregar una materia"""
