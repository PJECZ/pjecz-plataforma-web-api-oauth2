"""
Inventarios Custodias v1, esquemas
"""
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class InvCustodiaOut(BaseModel):
    """Esquema para entregar custodias"""

    id: int | None
    usuario_id: int | None
    usuario_email: str | None
    usuario_nombre: str | None
    fecha: date | None
    curp: str | None
    nombre_completo: str | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneInvCustodiaOut(InvCustodiaOut, OneBaseOut):
    """Esquema para entregar una custodia"""
