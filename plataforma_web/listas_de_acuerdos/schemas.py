"""
Listas de Acuerdos, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel


class ListaDeAcuerdo(BaseModel):
    """Esquema para consultar Listas de Acuerdos"""

    id: int
    distrito_id: int
    distrito: str
    autoridad_id: int
    autoridad: str
    fecha: date
    descripcion: str
    archivo: str
    url: str
