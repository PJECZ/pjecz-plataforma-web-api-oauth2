"""
Permisos v1, esquemas
"""
from datetime import date
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class PermisoOut(BaseModel):
    """Esquema para entregar permisos"""

    id: int | None
    rol_id: int | None
    rol_nombre: str | None
    modulo_id: int | None
    modulo_nombre: str | None
    nombre: str | None
    nivel: int | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OnePermisoOut(PermisoOut, OneBaseOut):
    """Esquema para entregar un permiso"""
