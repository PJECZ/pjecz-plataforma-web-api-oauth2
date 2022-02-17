"""
Permisos v1, esquemas de pydantic
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel


class PermisoOut(BaseModel):
    """Esquema para entregar permisos"""

    id: int
    rol_id: int
    rol_nombre: str
    modulo_id: int
    modulo_nombre: str
    nombre: str
    nivel: int

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
