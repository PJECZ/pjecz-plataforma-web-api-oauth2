"""
Usuarios v1, esquemas
"""
from datetime import datetime
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class UsuarioOut(BaseModel):
    """Esquema para entregar usuario"""

    id: int | None
    autoridad_id: int | None
    autoridad_clave: str | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    distrito_id: int | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    oficina_id: int | None
    oficina_clave: str | None
    email: str | None
    nombres: str | None
    apellido_paterno: str | None
    apellido_materno: str | None
    curp: str | None
    puesto: str | None
    telefono: str | None
    extension: str | None
    workspace: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneUsuarioOut(UsuarioOut, OneBaseOut):
    """Esquema para entregar un usuario"""


class UsuarioInDB(UsuarioOut):
    """Usuario en base de datos"""

    username: str
    permissions: dict
    hashed_password: str
    disabled: bool
    api_key: str
    api_key_expiracion: datetime
