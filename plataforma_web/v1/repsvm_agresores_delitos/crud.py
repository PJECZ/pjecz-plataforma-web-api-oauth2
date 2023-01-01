"""
REPSVM Agresores-Delitos v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import REPSVMAgresorDelito
from ..repsvm_agresores.crud import get_repsvm_agresor
from ..repsvm_delitos.crud import get_repsvm_delito


def get_repsvm_agresores_delitos(
    db: Session,
    estatus: str = None,
    repsvm_agresor_id: int = None,
    repsvm_delito_id: int = None,
) -> Any:
    """Consultar los agresores-delitos activos"""
    consulta = db.query(REPSVMAgresorDelito)
    if repsvm_agresor_id is not None and repsvm_agresor_id != 0:
        repsvm_agresor = get_repsvm_agresor(db, repsvm_agresor_id=repsvm_agresor_id)
        consulta = consulta.filter(REPSVMAgresorDelito.repsvm_agresor == repsvm_agresor)
    if repsvm_delito_id is not None and repsvm_delito_id != 0:
        repsvm_delito = get_repsvm_delito(db, repsvm_delito_id=repsvm_delito_id)
        consulta = consulta.filter(REPSVMAgresorDelito.repsvm_delito == repsvm_delito)
    return consulta.filter_by(estatus="A").order_by(REPSVMAgresorDelito.id)


def get_repsvm_agresor_delito(db: Session, repsvm_agresor_delito_id: int) -> REPSVMAgresorDelito:
    """Consultar un agresor-delito por su id"""
    repsvm_agresor_delito = db.query(REPSVMAgresorDelito).get(repsvm_agresor_delito_id)
    if repsvm_agresor_delito is None:
        raise PWNotExistsError("No existe ese agresor-delito")
    if repsvm_agresor_delito.estatus != "A":
        raise PWIsDeletedError("No es activo ese agresor-delito, está eliminado")
    return repsvm_agresor_delito
