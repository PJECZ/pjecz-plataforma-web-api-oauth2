"""
Modulos v1, esquemas de pydantic
"""
from pydantic import BaseModel


class ModuloOut(BaseModel):
    """Esquema para entregar modulos"""

    id: int
    nombre: str
    nombre_corto: str
    icono: str
    ruta: str
    en_navegacion: bool

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
