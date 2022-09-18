"""
Modulos v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import Modulo


def get_modulos(db: Session) -> Any:
    """Consultar los modulos activos"""
    return db.query(Modulo).filter_by(estatus="A").order_by(Modulo.nombre.asc())


def get_modulo(db: Session, modulo_id: int) -> Modulo:
    """Consultar un modulo por su id"""
    modulo = db.query(Modulo).get(modulo_id)
    if modulo is None:
        raise PWNotExistsError("No existe ese moódulo")
    if modulo.estatus != "A":
        raise PWIsDeletedError("No es activo ese módulo, está eliminado")
    return modulo
