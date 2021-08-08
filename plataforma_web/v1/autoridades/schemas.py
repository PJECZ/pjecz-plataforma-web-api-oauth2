"""
Autoridades v1.0, esquemas
"""
from pydantic import BaseModel


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridad"""

    id: int
    clave: str
    distrito_id: int
    materia_id: int
    descripcion: str
    descripcion_corta: str
    es_jurisdiccional: bool
    es_notaria: bool
    organo_jurisdiccional: str
    audiencia_categoria: str

    class Config:
        """SQLAlchemy config"""
        orm_mode = True
