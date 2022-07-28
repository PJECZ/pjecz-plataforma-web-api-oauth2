"""
Roles v1.0, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import Rol


def get_roles(db: Session) -> Any:
    """Consultar los roles activos"""
    return db.query(Rol).filter_by(estatus="A").order_by(Rol.nombre.asc())


def get_rol(db: Session, rol_id: int) -> Rol:
    """Consultar un rol por su id"""
    rol = db.query(Rol).get(rol_id)
    if rol is None:
        raise NotExistsException("No existe ese rol")
    if rol.estatus != "A":
        raise IsDeletedException("No es activo el rol, está eliminado")
    return rol
