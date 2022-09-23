"""
Usuarios Roles v1, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class UsuarioRolOut(BaseModel):
    """Esquema para entregar usuario-rol"""

    id: int | None
    rol_id: int | None
    rol_nombre: str | None
    usuario_id: int | None
    usuario_nombre: str | None
    descripcion: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneUsuarioRolOut(UsuarioRolOut, OneBaseOut):
    """Esquema para entregar un usuario-rol"""
