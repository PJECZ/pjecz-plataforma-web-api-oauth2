"""
Materias, esquemas de pydantic
"""
from pydantic import BaseModel


class Materia(BaseModel):
    """ Esquema para consultar materias """

    id: int
    materia: str
