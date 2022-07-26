"""
Inventarios Modelos v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import InvModelo
from ..inv_marcas.crud import get_inv_marca


def get_inv_modelos(
    db: Session,
    inv_marca_id: int = None,
) -> Any:
    """Consultar los modelos activos"""
    consulta = db.query(InvModelo)
    if inv_marca_id:
        inv_marca = get_inv_marca(db, inv_marca_id=inv_marca_id)
        consulta = consulta.filter(InvModelo.inv_marca == inv_marca)
    return consulta.filter_by(estatus="A").order_by(InvModelo.id)


def get_inv_modelo(db: Session, inv_modelo_id: int) -> InvModelo:
    """Consultar un modelo por su id"""
    inv_modelo = db.query(InvModelo).get(inv_modelo_id)
    if inv_modelo is None:
        raise IndexError("No existe ese modelo")
    if inv_modelo.estatus != "A":
        raise ValueError("No es activo ese modelo, está eliminado")
    return inv_modelo
