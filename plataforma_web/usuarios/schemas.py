"""
Usuarios, esquemas de pydantic
"""
from typing import Optional
from pydantic import BaseModel


class Usuario(BaseModel):
    """Usuario"""

    id: int
    distrito_id: int
    distrito: str
    autoridad_id: int
    autoridad: str
    rol_id: int
    rol: str
    email: str
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None


class UsuarioEnBD(Usuario):
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
