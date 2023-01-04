"""
Distritos v1, esquemas
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distrito"""

    id: int | None
    nombre: str | None
    nombre_corto: str | None
    es_distrito_judicial: bool | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneDistritoOut(DistritoOut, OneBaseOut):
    """Esquema para entregar un distrito"""
