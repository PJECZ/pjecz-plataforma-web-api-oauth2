"""
Listas de Acuerdos Acuerdos, esquemas de pydantic
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel


class ListaDeAcuerdoAcuerdoNew(BaseModel):
    """Acuerdo de Listas de Acuerdos nuevo"""

    id: int
    lista_de_acuerdo_id: int
    fecha: date
    folio: Optional[str] = ""
    expediente: Optional[str] = ""
    actor: str
    demandado: str
    tipo_acuerdo: str
    tipo_juicio: str


class ListaDeAcuerdoAcuerdo(ListaDeAcuerdoAcuerdoNew):
    """Acuerdo de Listas de Acuerdos"""

    id: int
