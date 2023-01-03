"""
Domicilios v1, esquemas
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class DomicilioOut(BaseModel):
    """Esquema para entregar domicilios"""

    id: int | None
    edificio: str | None
    estado: str | None
    municipio: str | None
    calle: str | None
    num_ext: str | None
    num_int: str | None
    colonia: str | None
    cp: int | None
    completo: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneDomicilioOut(DomicilioOut, OneBaseOut):
    """Esquema para entregar un domicilio"""
