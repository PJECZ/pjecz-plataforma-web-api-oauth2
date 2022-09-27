"""
Inventarios Modelos v1, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class InvModeloOut(BaseModel):
    """Esquema para entregar modelos"""

    id: int | None
    inv_marca_id: int | None
    inv_marca_nombre: str | None
    descripcion: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneInvModeloOut(InvModeloOut, OneBaseOut):
    """Esquema para entregar un modelo"""
