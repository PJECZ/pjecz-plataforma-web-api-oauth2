"""
Usuarios Roles v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from .models import UsuarioRol
from ..roles.crud import get_rol
from ..usuarios.crud import get_usuario


def get_usuarios_roles(
    db: Session,
    rol_id: int = None,
    usuario_id: int = None,
) -> Any:
    """Consultar los usuarios_roles activos"""
    consulta = db.query(UsuarioRol)
    if rol_id:
        rol = get_rol(db, rol_id)
        consulta = consulta.filter(UsuarioRol.rol == rol)
    if usuario_id:
        usuario = get_usuario(db, usuario_id)
        consulta = consulta.filter_by(UsuarioRol.usuario == usuario)
    return consulta.filter_by(estatus="A").order_by(UsuarioRol.id.desc())


def get_usuario_rol(db: Session, usuario_rol_id: int) -> UsuarioRol:
    """Consultar un usuario_rol por su id"""
    usuario_rol = db.query(UsuarioRol).get(usuario_rol_id)
    if usuario_rol is None:
        raise IndexError("No existe ese usuario-rol")
    if usuario_rol.estatus != "A":
        raise ValueError("No es activo ese usuario-rol, está eliminado")
    return usuario_rol
