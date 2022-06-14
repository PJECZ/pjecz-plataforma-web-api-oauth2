"""
Inventarios Componentes v1, esquemas de pydantic
"""
from typing import Optional
from pydantic import BaseModel


class InvComponenteOut(BaseModel):
    """Esquema para entregar componentes"""

    id: int
    inv_categoria_id: int
    inv_categoria_nombre: str
    inv_equipo_id: int
    inv_equipo_descripcion: str
    descripcion: str
    cantidad: int
    generacion: str
    version: Optional[str] = ""

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
