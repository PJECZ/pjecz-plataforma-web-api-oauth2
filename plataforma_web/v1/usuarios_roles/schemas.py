"""
Usuarios Roles v1, esquemas de pydantic
"""
from pydantic import BaseModel


class UsuarioRolOut(BaseModel):
    """ Esquema para entregar usuario-rol """

    id: int
    rol_id: int
    rol_nombre: str
    usuario_id: int
    usuario_nombre: str
    descripcion: str

    class Config:
        """ SQLAlchemy config """

        orm_mode = True
