"""
Soportes Categorias v1, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class SoporteCategoriaOut(BaseModel):
    """Esquema para entregar soporte categoria"""

    id: int | None
    rol_id: int | None
    rol_nombre: str | None
    nombre: str | None
    instrucciones: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneSoporteCategoriaOut(SoporteCategoriaOut, OneBaseOut):
    """Esquema para entregar una categoria de soporte"""
