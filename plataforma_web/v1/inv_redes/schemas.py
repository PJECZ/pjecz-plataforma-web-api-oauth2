"""
Inventarios Redes v1, esquemas de pydantic
"""
from pydantic import BaseModel


class InvRedOut(BaseModel):
    """Esquema para entregar redes"""

    id: int
    nombre: str
    tipo: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
