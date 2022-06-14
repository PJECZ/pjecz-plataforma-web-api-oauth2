"""
Inventarios Categorias v1, esquemas de pydantic
"""
from pydantic import BaseModel


class InvCategoriaOut(BaseModel):
    """Esquema para entregar categorias"""

    id: int
    nombre: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
