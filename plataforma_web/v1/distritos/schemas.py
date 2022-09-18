"""
Distritos v1.0, esquemas
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distrito"""

    id: int
    nombre: str
    nombre_corto: str
    es_distrito_judicial: bool

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneDistritoOut(DistritoOut, OneBaseOut):
    """Esquema para entregar un distrito"""
