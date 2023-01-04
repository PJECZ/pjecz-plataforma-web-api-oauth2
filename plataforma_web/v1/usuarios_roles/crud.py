"""
Usuarios Roles v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from ...core.usuarios_roles.models import UsuarioRol
from ..roles.crud import get_rol
from ..usuarios.crud import get_usuario


def get_usuarios_roles(
    db: Session,
    estatus: str = None,
    rol_id: int = None,
    usuario_id: int = None,
) -> Any:
    """Consultar los usuarios roles"""

    # Consultar
    consulta = db.query(UsuarioRol)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por rol
    if rol_id is not None:
        rol = get_rol(db, rol_id)
        consulta = consulta.filter(UsuarioRol.rol == rol)

    # Filtrar por usuario
    if usuario_id is not None:
        usuario = get_usuario(db, usuario_id)
        consulta = consulta.filter_by(UsuarioRol.usuario == usuario)

    # Entregar
    return consulta.order_by(UsuarioRol.descripcion)


def get_usuario_rol(db: Session, usuario_rol_id: int) -> UsuarioRol:
    """Consultar un usuario_rol por su id"""
    usuario_rol = db.query(UsuarioRol).get(usuario_rol_id)
    if usuario_rol is None:
        raise PWNotExistsError("No existe ese usuario-rol")
    if usuario_rol.estatus != "A":
        raise PWIsDeletedError("No es activo ese usuario-rol, está eliminado")
    return usuario_rol
