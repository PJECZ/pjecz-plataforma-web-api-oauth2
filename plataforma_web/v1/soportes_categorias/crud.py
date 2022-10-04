"""
Soportes Categorias v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import SoporteCategoria


def get_soportes_categorias(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los soportes_categorias"""
    
    # Consultar
    consulta = db.query(SoporteCategoria)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(SoporteCategoria.nombre)


def get_soporte_categoria(db: Session, soporte_categoria_id: int) -> SoporteCategoria:
    """Consultar un soporte_categoria por su id"""
    soporte_categoria = db.query(SoporteCategoria).get(soporte_categoria_id)
    if soporte_categoria is None:
        raise PWNotExistsError("No existe esa categoria")
    if soporte_categoria.estatus != "A":
        raise PWIsDeletedError("No es activa esa categoria, está eliminado")
    return soporte_categoria
