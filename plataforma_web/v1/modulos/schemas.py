"""
Modulos v1, esquemas
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class ModuloOut(BaseModel):
    """Esquema para entregar modulos"""

    id: int | None
    nombre: str | None
    nombre_corto: str | None
    icono: str | None
    ruta: str | None
    en_navegacion: bool | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneModuloOut(ModuloOut, OneBaseOut):
    """Esquema para entregar un modulo"""
