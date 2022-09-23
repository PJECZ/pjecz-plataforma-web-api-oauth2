"""
Autoridades v1, esquemas
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridad"""

    id: int | None
    distrito_id: int | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    materia_id: int | None
    materia_nombre: str | None
    clave: str | None
    descripcion: str | None
    descripcion_corta: str | None
    es_jurisdiccional: bool | None
    es_notaria: bool | None
    organo_jurisdiccional: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneAutoridadOut(AutoridadOut, OneBaseOut):
    """Esquema para entregar un autoridad"""
