"""
REDAM (Registro Estatal de Deudores Alimentarios) v1, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class RedamOut(BaseModel):
    """Esquema para entregar deudores"""

    id: int | None
    distrito_id: int | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    autoridad_clave: str | None
    nombre: str | None
    expediente: str | None
    fecha: date | None
    observaciones: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneRedamOut(RedamOut, OneBaseOut):
    """Esquema para entregar un redam"""
