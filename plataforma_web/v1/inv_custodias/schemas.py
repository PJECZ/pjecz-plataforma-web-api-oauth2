"""
Inventarios Custodias v1, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel


class InvCustodiaOut(BaseModel):
    """Esquema para entregar custodias"""

    id: int
    usuario_id: int
    usuario_nombre: str
    fecha: date
    curp: str
    nombre_completo: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
