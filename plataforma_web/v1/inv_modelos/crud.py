"""
Inventarios Modelos v1, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from ...core.inv_marcas.models import InvMarca
from ...core.inv_modelos.models import InvModelo
from ..inv_marcas.crud import get_inv_marca


def get_inv_modelos(
    db: Session,
    estatus: str = None,
    inv_marca_id: int = None,
) -> Any:
    """Consultar los modelos"""

    # Consultar
    consulta = db.query(InvModelo).join(InvMarca)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por marca
    if inv_marca_id:
        inv_marca = get_inv_marca(db, inv_marca_id=inv_marca_id)
        consulta = consulta.filter(InvModelo.inv_marca == inv_marca)

    # Entregar
    return consulta.order_by(InvMarca.nombre, InvModelo.descripcion)


def get_inv_modelo(db: Session, inv_modelo_id: int) -> InvModelo:
    """Consultar un modelo por su id"""
    inv_modelo = db.query(InvModelo).get(inv_modelo_id)
    if inv_modelo is None:
        raise PWNotExistsError("No existe ese modelo")
    if inv_modelo.estatus != "A":
        raise PWIsDeletedError("No es activo ese modelo, está eliminado")
    return inv_modelo
