"""
Inventarios Marcas v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import InvMarca


def get_inv_marcas(db: Session) -> Any:
    """Consultar las marcas activas"""
    return db.query(InvMarca).filter_by(estatus="A").order_by(InvMarca.id)


def get_inv_marca(db: Session, inv_marca_id: int) -> InvMarca:
    """Consultar una marca por su id"""
    inv_marca = db.query(InvMarca).get(inv_marca_id)
    if inv_marca is None:
        raise NotExistsException("No existe ese marca")
    if inv_marca.estatus != "A":
        raise IsDeletedException("No es activo ese marca, está eliminado")
    return inv_marca
