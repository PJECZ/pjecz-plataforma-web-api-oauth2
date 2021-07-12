"""
Listas de Acuerdos Acuerdos, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel


class ListaDeAcuerdoAcuerdo(BaseModel):
    """Esquema para consultar acuerdos"""

    id: int
    lista_de_acuerdo_id: int
    fecha: date
    folio: str
    expediente: str
    actor: str
    demandado: str
    tipo_acuerdo: str
    tipo_juicio: str
