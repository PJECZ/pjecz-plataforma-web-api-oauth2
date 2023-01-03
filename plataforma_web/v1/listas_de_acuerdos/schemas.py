"""
Listas de Acuerdos v1, esquemas
"""
from datetime import datetime, date
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ListaDeAcuerdoIn(BaseModel):
    """Esquema para recibir lista de acuerdo"""

    autoridad_id: int | None
    fecha: date | None
    descripcion: str | None


class ListaDeAcuerdoOut(ListaDeAcuerdoIn):
    """Esquema para entregar lista de acuerdo"""

    id: int | None
    distrito_id: int | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    autoridad_clave: str | None
    archivo: str | None
    url: str | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneListaDeAcuerdoOut(ListaDeAcuerdoOut, OneBaseOut):
    """Esquema para entregar una lista de acuerdos"""
