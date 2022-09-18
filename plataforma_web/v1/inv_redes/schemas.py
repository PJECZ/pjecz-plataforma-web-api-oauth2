"""
Inventarios Redes v1, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class InvRedOut(BaseModel):
    """Esquema para entregar redes"""

    id: int
    nombre: str
    tipo: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneInvRedOut(InvRedOut, OneBaseOut):
    """Esquema para entregar una red"""
