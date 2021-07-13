"""
Usuarios, esquemas de pydantic
"""
from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    """Esquema para usuarios"""

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
    """Usuario en BD"""

    hashed_password: str


class Token(BaseModel):
    """Token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data"""

    username: Optional[str] = None
