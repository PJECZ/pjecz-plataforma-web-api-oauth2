"""
Soportes Categorias v1, esquemas de pydantic
"""
from pydantic import BaseModel


class SoporteCategoria(BaseModel):
    """ Esquema para entregar Soporte Categoria """

    id: int
    rol_id: int
    rol_nombre: str
    nombre: str
    instrucciones: str

    class Config:
        """ SQLAlchemy config """

        orm_mode = True
