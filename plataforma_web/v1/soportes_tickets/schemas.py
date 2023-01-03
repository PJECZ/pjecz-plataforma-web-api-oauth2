"""
Soportes Tickets v1, esquemas
"""
from datetime import datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class SoporteTicketOut(BaseModel):
    """Esquema para entregar soporte ticket"""

    id: int | None
    funcionario_id: int | None
    funcionario_nombre: str | None
    soporte_categoria_id: int | None
    soporte_categoria_nombre: str | None
    usuario_id: int | None
    usuario_email: str | None
    usuario_nombre: str | None
    usuario_oficina_id: int | None
    usuario_oficina_clave: str | None
    descripcion: str | None
    estado: str | None
    soluciones: str | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneSoporteTicketOut(SoporteTicketOut, OneBaseOut):
    """Esquema para entregar un ticket de soporte"""


class SoporteTicketTotalOut(BaseModel):
    """Esquema para entregar totales de tickets por oficina y por categoria"""

    distrito_clave: str
    soporte_categoria_nombre: str
    cantidad: int
