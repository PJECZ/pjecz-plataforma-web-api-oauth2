"""
Centros de Trabajo v1, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CentroTrabajoOut(BaseModel):
    """Esquema para entregar centro de trabajo"""

    id: int | None
    distrito_id: int | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    domicilio_id: int | None
    domicilio_completo: str | None
    clave: str | None
    nombre: str | None
    telefono: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCentroTrabajoOut(CentroTrabajoOut, OneBaseOut):
    """Esquema para entregar un centro de trabajo"""
