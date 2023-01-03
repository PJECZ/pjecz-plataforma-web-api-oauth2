"""
REPSVM Delitos v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from ...core.repsvm_delitos.models import REPSVMDelito


def get_repsvm_delitos(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los delitos activos"""

    # Consultar
    consulta = db.query(REPSVMDelito)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(REPSVMDelito.id)


def get_repsvm_delito(db: Session, repsvm_delito_id: int) -> REPSVMDelito:
    """Consultar un delito por su id"""
    repsvm_delito = db.query(REPSVMDelito).get(repsvm_delito_id)
    if repsvm_delito is None:
        raise PWNotExistsError("No existe ese delito")
    if repsvm_delito.estatus != "A":
        raise PWIsDeletedError("No es activo ese delito, está eliminado")
    return repsvm_delito
