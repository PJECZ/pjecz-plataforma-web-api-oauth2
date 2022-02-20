"""
Oficinas v1, esquemas de pydantic
"""
from datetime import time
from pydantic import BaseModel


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    id: int
    domicilio_id: int
    domicilio_nombre: str
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
