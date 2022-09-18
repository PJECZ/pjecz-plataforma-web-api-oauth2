"""
Listas de Acuerdos, Acuerdos v1, esquemas de pydantic
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ListaDeAcuerdoAcuerdoIn(BaseModel):
    """Esquema para recibir acuerdo"""

    lista_de_acuerdo_id: int
    folio: Optional[str] = ""
    expediente: Optional[str] = ""
    actor: str
    demandado: str
    tipo_acuerdo: str
    tipo_juicio: str
    referencia: int


class ListaDeAcuerdoAcuerdoOut(ListaDeAcuerdoAcuerdoIn):
    """Esquema para entregar acuerdo"""

    id: int
    fecha: date

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneListaDeAcuerdoAcuerdoOut(ListaDeAcuerdoAcuerdoOut, OneBaseOut):
    """Esquema para entregar un acuerdo"""
