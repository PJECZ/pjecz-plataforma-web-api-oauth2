"""
Usuarios v1.0, esquemas
"""
from typing import Optional
from pydantic import BaseModel


class UsuarioOut(BaseModel):
    """Esquema para entregar usuario"""

    id: int
    rol_id: int
    rol_nombre: str
    distrito_id: int
    distrito_nombre: str
    distrito_nombre_corto: str
    autoridad_id: int
    autoridad_descripcion: str
    autoridad_descripcion_corta: str
    email: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class UsuarioInBD(UsuarioOut):
    """Usuario en base de datos"""

    username: str
    permissions: int
    hashed_password: str
    disabled: bool


class Token(BaseModel):
    """Token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data"""

    username: Optional[str] = None
