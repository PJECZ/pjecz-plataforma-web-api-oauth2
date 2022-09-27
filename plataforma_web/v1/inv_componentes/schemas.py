"""
Inventarios Componentes v1, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class InvComponenteOut(BaseModel):
    """Esquema para entregar componentes"""

    id: int | None
    inv_categoria_id: int | None
    inv_categoria_nombre: str | None
    inv_equipo_id: int | None
    inv_equipo_descripcion: str | None
    descripcion: str | None
    cantidad: int | None
    generacion: str | None
    version: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneInvComponenteOut(InvComponenteOut, OneBaseOut):
    """Esquema para entregar un componente"""
