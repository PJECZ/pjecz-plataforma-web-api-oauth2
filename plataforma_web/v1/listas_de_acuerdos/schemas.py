"""
Listas de Acuerdos v1, esquemas de pydantic
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel


class ListaDeAcuerdoIn(BaseModel):
    """ Esquema para recibir lista de acuerdo """

    autoridad_id: int
    fecha: date
    descripcion: str


class ListaDeAcuerdoOut(ListaDeAcuerdoIn):
    """ Esquema para entregar lista de acuerdo """

    id: int
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    autoridad_descripcion: str
    autoridad_descripcion_corta: str
    archivo: Optional[str] = ""
    url: Optional[str] = ""

    class Config:
        """ SQLAlchemy config """
        orm_mode = True
