"""
REDAM (Registro Estatal de Deudores Alimentarios) v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from .models import Redam


def get_redams(db: Session) -> Any:
    """Consultar los deudores activos"""
    consulta = db.query(Redam)
    return consulta.filter_by(estatus="A").order_by(Redam.id)


def get_redam(db: Session, redam_id: int) -> Redam:
    """Consultar un deudor por su id"""
    redam = db.query(Redam).get(redam_id)
    if redam is None:
        raise IndexError("No existe ese deudor")
    if redam.estatus != "A":
        raise ValueError("No es activo ese deudor, está eliminado")
    return redam
