"""
Roles, esquemas de pydantic
"""
from pydantic import BaseModel


class Rol(BaseModel):
    """Esquema para roles"""

    id: int
    rol: str
