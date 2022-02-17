"""
Soportes Categorias v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from plataforma_web.v1.soportes_categorias.models import SoporteCategoria


def get_soportes_categorias(db: Session) -> Any:
    """Consultar los soportes_categorias activos"""
    return db.query(SoporteCategoria).filter_by(estatus="A").order_by(SoporteCategoria.nombre)


def get_soporte_categoria(db: Session, soporte_categoria_id: int) -> SoporteCategoria:
    """Consultar un soporte_categoria por su id"""
    soporte_categoria = db.query(SoporteCategoria).get(soporte_categoria_id)
    if soporte_categoria is None:
        raise IndexError("No existe esa categoria")
    if soporte_categoria.estatus != "A":
        raise ValueError("No es activa esa categoria, está eliminado")
    return soporte_categoria
