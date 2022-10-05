"""
Materias v1.0, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import Materia


def get_materias(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar las materias"""

    # Consultar
    consulta = db.query(Materia)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(Materia.nombre)


def get_materia(
    db: Session,
    materia_id: int,
) -> Materia:
    """Consultar un materia por su id"""
    materia = db.query(Materia).get(materia_id)
    if materia is None:
        raise PWNotExistsError("No existe esa materia")
    if materia.estatus != "A":
        raise PWIsDeletedError("No es activa la materia, está eliminada")
    return materia
