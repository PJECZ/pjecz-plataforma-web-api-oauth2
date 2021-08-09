"""
Distritos v1.0, esquemas
"""
from pydantic import BaseModel


class DistritoOut(BaseModel):
    """Esquema para entregar distrito"""

    id: int
    nombre: str
    nombre_corto: str
    es_distrito_judicial: bool

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
