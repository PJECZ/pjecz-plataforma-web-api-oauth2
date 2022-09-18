"""
Listas de Acuerdos v1, esquemas de pydantic
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ListaDeAcuerdoIn(BaseModel):
    """Esquema para recibir lista de acuerdo"""

    autoridad_id: int
    fecha: date
    descripcion: str


class ListaDeAcuerdoOut(ListaDeAcuerdoIn):
    """Esquema para entregar lista de acuerdo"""

    id: int
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    autoridad_descripcion: str
    autoridad_descripcion_corta: str
    autoridad_clave: str
    archivo: Optional[str] = ""
    url: Optional[str] = ""
    creado: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneListaDeAcuerdoOut(ListaDeAcuerdoOut, OneBaseOut):
    """Esquema para entregar una lista de acuerdos"""
