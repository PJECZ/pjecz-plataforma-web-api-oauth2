"""
Inventarios Redes v1, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import InvRed


def get_inv_redes(db: Session) -> Any:
    """Consultar las redes activas"""
    return db.query(InvRed).filter_by(estatus="A").order_by(InvRed.id)


def get_inv_red(db: Session, inv_red_id: int) -> InvRed:
    """Consultar una red por su id"""
    inv_red = db.query(InvRed).get(inv_red_id)
    if inv_red is None:
        raise NotExistsException("No existe ese red")
    if inv_red.estatus != "A":
        raise IsDeletedException("No es activo ese red, está eliminado")
    return inv_red
