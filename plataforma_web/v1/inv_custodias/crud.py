"""
Inventarios Custodias v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from .models import InvCustodia


def get_inv_custodias(
    db: Session,
) -> Any:
    """Consultar los custodias activos"""
    consulta = db.query(InvCustodia)
    return consulta.filter_by(estatus="A").order_by(InvCustodia.id)


def get_inv_custodia(db: Session, inv_custodia_id: int) -> InvCustodia:
    """Consultar un custodia por su id"""
    inv_custodia = db.query(InvCustodia).get(inv_custodia_id)
    if inv_custodia is None:
        raise IndexError("No existe ese custodia")
    if inv_custodia.estatus != "A":
        raise ValueError("No es activo ese custodia, está eliminado")
    return inv_custodia
