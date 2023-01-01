"""
REPSVM Agresores v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError
from lib.safe_string import safe_string

from .models import REPSVMAgresor
from ..distritos.crud import get_distrito


def get_repsvm_agresores(
    db: Session,
    distrito_id: int = None,
    estatus: str = None,
    nombre: str = None,
) -> Any:
    """Consultar los agresores activos"""

    # Consultar
    consulta = db.query(REPSVMAgresor)

    # Filtrar por distrito
    if distrito_id:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter(distrito=distrito)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por nombre
    if nombre is not None:
        nombre = safe_string(nombre)
        if nombre != "":
            consulta = consulta.filter_by(nombre=nombre)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(REPSVMAgresor.nombre)


def get_repsvm_agresor(db: Session, repsvm_agresor_id: int) -> REPSVMAgresor:
    """Consultar un agresor por su id"""
    repsvm_agresor = db.query(REPSVMAgresor).get(repsvm_agresor_id)
    if repsvm_agresor is None:
        raise PWNotExistsError("No existe ese agresor")
    if repsvm_agresor.estatus != "A":
        raise PWIsDeletedError("No es activo ese agresor, está eliminado")
    return repsvm_agresor
