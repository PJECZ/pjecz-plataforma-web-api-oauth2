"""
Modulos v1, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


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


class OneModuloOut(ModuloOut, OneBaseOut):
    """Esquema para entregar un modulo"""
