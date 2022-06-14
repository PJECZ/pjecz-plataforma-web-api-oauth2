"""
Inventarios Modelos v1, esquemas de pydantic
"""
from pydantic import BaseModel


class InvModeloOut(BaseModel):
    """Esquema para entregar modelos"""

    id: int
    marca_id: int
    marca_nombre: str
    descripcion: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
