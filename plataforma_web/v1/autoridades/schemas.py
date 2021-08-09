"""
Autoridades v1, esquemas
"""
from pydantic import BaseModel


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridad"""

    id: int
    clave: str
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    materia_id: int
    materia_nombre: str
    descripcion: str
    descripcion_corta: str
    es_jurisdiccional: bool
    es_notaria: bool
    organo_jurisdiccional: str
    audiencia_categoria: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
