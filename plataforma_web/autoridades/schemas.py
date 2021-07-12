"""
Autoridades, esquemas de pydantic
"""
from pydantic import BaseModel


class Autoridad(BaseModel):
    """ Esquema Autoridad para listado """

    id: int
    distrito_id: int
    distrito: str
    materia_id: int
    materia: str
    autoridad: str
    autoridad_corta: str
    organo_jurisdiccional: str
    audiencia_categoria: str
