"""
Inventarios Categorias v1, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import InvCategoria


def get_inv_categorias(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar las categorias"""

    # Consultar
    consulta = db.query(InvCategoria)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(InvCategoria.nombre)


def get_inv_categoria(
    db: Session,
    inv_categoria_id: int,
) -> InvCategoria:
    """Consultar una categoria por su id"""
    inv_categoria = db.query(InvCategoria).get(inv_categoria_id)
    if inv_categoria is None:
        raise PWNotExistsError("No existe ese categoria")
    if inv_categoria.estatus != "A":
        raise PWIsDeletedError("No es activo ese categoria, está eliminado")
    return inv_categoria
