"""
Usuarios v1.0, esquemas
"""
from typing import Optional
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class UsuarioOut(BaseModel):
    """Esquema para entregar usuario"""

    id: int
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    autoridad_id: int
    autoridad_clave: str
    autoridad_descripcion: str
    autoridad_descripcion_corta: str
    oficina_id: int
    oficina_clave: str
    email: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    curp: str
    puesto: str
    telefono_celular: str

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


class Token(BaseModel):
    """Token"""

    access_token: str
    token_type: str
    username: str


class TokenData(BaseModel):
    """Token data"""

    username: Optional[str] = None
