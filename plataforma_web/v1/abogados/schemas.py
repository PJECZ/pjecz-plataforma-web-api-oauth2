"""
Abogados v1, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class AbogadoOut(BaseModel):
    """Esquema para entregar abogados"""

    id: int
    fecha: date
    libro: str
    numero: str
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneAbogadoOut(AbogadoOut, OneBaseOut):
    """Esquema para entregar un abogado"""
