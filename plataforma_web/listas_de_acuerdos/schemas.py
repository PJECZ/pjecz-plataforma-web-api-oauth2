"""
Listas de Acuerdos, esquemas de pydantic
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel


class ListaDeAcuerdoNew(BaseModel):
    """Lista de Acuerdos nueva"""

    autoridad_id: int
    fecha: date
    descripcion: str
    archivo: Optional[str] = ""
    url: Optional[str] = ""


class ListaDeAcuerdo(BaseModel):
    """Lista de Acuerdos"""

    id: int
    distrito_id: int
    distrito: str
    autoridad_id: int
    autoridad: str
    fecha: date
    descripcion: str
    archivo: Optional[str] = ""
    url: Optional[str] = ""
