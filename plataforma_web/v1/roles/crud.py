"""
Roles v1.0, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import Rol


def get_roles(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los roles activos"""

    # Consultar
    consulta = db.query(Rol)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(Rol.nombre)


def get_rol(
    db: Session,
    rol_id: int,
) -> Rol:
    """Consultar un rol por su id"""
    rol = db.query(Rol).get(rol_id)
    if rol is None:
        raise PWNotExistsError("No existe ese rol")
    if rol.estatus != "A":
        raise PWIsDeletedError("No es activo el rol, está eliminado")
    return rol
