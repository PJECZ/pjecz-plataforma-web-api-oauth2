"""
Distritos, esquemas de pydantic
"""
from pydantic import BaseModel


class Distrito(BaseModel):
    """ Esquema Distrito """

    id: int
    distrito: str
    distrito_corto: str
