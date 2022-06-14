"""
Inventarios Marcas v1, esquemas de pydantic
"""
from pydantic import BaseModel


class InvMarcaOut(BaseModel):
    """Esquema para entregar marcas"""

    id: int
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
