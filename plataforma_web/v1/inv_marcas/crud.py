"""
Inventarios Marcas v1, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from ...core.inv_marcas.models import InvMarca


def get_inv_marcas(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar las marcas"""

    # Consultar
    consulta = db.query(InvMarca)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(InvMarca.nombre)


def get_inv_marca(
    db: Session,
    inv_marca_id: int,
) -> InvMarca:
    """Consultar una marca por su id"""
    inv_marca = db.query(InvMarca).get(inv_marca_id)
    if inv_marca is None:
        raise PWNotExistsError("No existe ese marca")
    if inv_marca.estatus != "A":
        raise PWIsDeletedError("No es activo ese marca, está eliminado")
    return inv_marca
