"""
Usuarios, esquemas de pydantic
"""
from pydantic import BaseModel


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
    apellido_materno: str
