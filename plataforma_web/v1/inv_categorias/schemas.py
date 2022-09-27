"""
Inventarios Categorias v1, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class InvCategoriaOut(BaseModel):
    """Esquema para entregar categorias"""

    id: int | None
    nombre: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneInvCategoriaOut(InvCategoriaOut, OneBaseOut):
    """Esquema para entregar una categoria"""
