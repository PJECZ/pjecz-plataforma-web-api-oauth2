"""
Listas de Acuerdos, Acuerdos v1, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ListaDeAcuerdoAcuerdoIn(BaseModel):
    """Esquema para recibir acuerdo"""

    lista_de_acuerdo_id: int | None
    folio: str | None
    expediente: str | None
    actor: str | None
    demandado: str | None
    tipo_acuerdo: str | None
    tipo_juicio: str | None
    referencia: int | None


class ListaDeAcuerdoAcuerdoOut(ListaDeAcuerdoAcuerdoIn):
    """Esquema para entregar acuerdo"""

    id: int | None
    fecha: date | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneListaDeAcuerdoAcuerdoOut(ListaDeAcuerdoAcuerdoOut, OneBaseOut):
    """Esquema para entregar un acuerdo"""
