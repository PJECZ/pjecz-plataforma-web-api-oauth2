"""
Inventarios Custodias v1, esquemas de pydantic
"""
from datetime import date, datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class InvCustodiaOut(BaseModel):
    """Esquema para entregar custodias"""

    id: int
    usuario_id: int
    usuario_email: str
    usuario_nombre: str
    fecha: date
    curp: str
    nombre_completo: str
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneInvCustodiaOut(InvCustodiaOut, OneBaseOut):
    """Esquema para entregar una custodia"""
