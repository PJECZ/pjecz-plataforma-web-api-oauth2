"""
Modulos v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import Modulo


def get_modulos(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los modulos activos"""

    # Consultar
    consulta = db.query(Modulo)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(Modulo.nombre)


def get_modulo(
    db: Session,
    modulo_id: int,
) -> Modulo:
    """Consultar un modulo por su id"""
    modulo = db.query(Modulo).get(modulo_id)
    if modulo is None:
        raise PWNotExistsError("No existe ese moódulo")
    if modulo.estatus != "A":
        raise PWIsDeletedError("No es activo ese módulo, está eliminado")
    return modulo
