"""
Inventarios Redes v1, esquemas
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class InvRedOut(BaseModel):
    """Esquema para entregar redes"""

    id: int | None
    nombre: str | None
    tipo: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneInvRedOut(InvRedOut, OneBaseOut):
    """Esquema para entregar una red"""
