"""
Domicilios v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import Domicilio


def get_domicilios(db: Session) -> Any:
    """Consultar los domicilios activos"""
    return db.query(Domicilio).filter_by(estatus="A").order_by(Domicilio.id.desc())


def get_domicilio(db: Session, domicilio_id: int) -> Domicilio:
    """Consultar un domicilio por su id"""
    domicilio = db.query(Domicilio).get(domicilio_id)
    if domicilio is None:
        raise PWNotExistsError("No existe ese domicilio")
    if domicilio.estatus != "A":
        raise PWIsDeletedError("No es activo ese domicilio, está eliminado")
    return domicilio
