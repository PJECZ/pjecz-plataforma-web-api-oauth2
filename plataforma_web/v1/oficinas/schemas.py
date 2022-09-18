"""
Oficinas v1, esquemas de pydantic
"""
from datetime import time
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    id: int
    domicilio_id: int
    domicilio_completo: str
    clave: str
    descripcion: str
    descripcion_corta: str
    es_jurisdiccional: bool
    apertura: time
    cierre: time
    limite_personas: int

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneOficinaOut(OficinaOut, OneBaseOut):
    """Esquema para entregar una oficina"""
