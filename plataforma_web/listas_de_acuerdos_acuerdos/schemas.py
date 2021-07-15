"""
Listas de Acuerdos Acuerdos, esquemas de pydantic
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel


class ListaDeAcuerdoAcuerdoNew(BaseModel):
    """Acuerdo de Listas de Acuerdos nuevo"""

    lista_de_acuerdo_id: int
    fecha: date
    folio: Optional[str] = ""
    expediente: Optional[str] = ""
    actor: str
    demandado: str
    tipo_acuerdo: str
    tipo_juicio: str
    referencia: int


class ListaDeAcuerdoAcuerdo(ListaDeAcuerdoAcuerdoNew):
    """Acuerdo de Listas de Acuerdos"""

    id: int
    distrito_id: int
    distrito: str
    autoridad_id: int
    autoridad: str
