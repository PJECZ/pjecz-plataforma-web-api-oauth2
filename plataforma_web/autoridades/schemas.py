"""
Autoridades, esquemas de pydantic
"""
from pydantic import BaseModel


class Autoridad(BaseModel):
    """Esquema para autoridades"""

    id: int
    clave: str
    distrito_id: int
    # distrito: str
    materia_id: int
    # materia: str
    descripcion: str
    descripcion_corta: str
    organo_jurisdiccional: str
    audiencia_categoria: str


class AutoridadOut(Autoridad):
    """Esquema paginado para autoridades"""

    class Config:
        orm_mode = True
