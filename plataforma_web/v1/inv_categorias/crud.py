"""
Inventarios Categorias v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from .models import InvCategoria


def get_inv_categorias(db: Session) -> Any:
    """Consultar las categorias activas"""
    return db.query(InvCategoria).filter_by(estatus="A").order_by(InvCategoria.id)


def get_inv_categoria(db: Session, inv_categoria_id: int) -> InvCategoria:
    """Consultar una categoria por su id"""
    inv_categoria = db.query(InvCategoria).get(inv_categoria_id)
    if inv_categoria is None:
        raise IndexError("No existe ese categoria")
    if inv_categoria.estatus != "A":
        raise ValueError("No es activo ese categoria, está eliminado")
    return inv_categoria
