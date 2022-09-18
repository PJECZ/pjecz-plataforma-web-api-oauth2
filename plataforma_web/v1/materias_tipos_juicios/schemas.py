"""
Materias Tipos Juicios v1, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class MateriaTipoJuicioOut(BaseModel):
    """Esquema para entregar tipo de juicio"""

    id: int
    materia_id: int
    materia_nombre: str
    descripcion: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneMateriaTipoJuicioOut(MateriaTipoJuicioOut, OneBaseOut):
    """Esquema para entregar un tipo de juicio"""
