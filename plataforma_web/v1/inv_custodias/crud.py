"""
Inventarios Custodias v1, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import InvCustodia
from ..usuarios.crud import get_usuario, get_usuario_from_email


def get_inv_custodias(
    db: Session,
    estatus: str = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar los custodias activos"""
    consulta = db.query(InvCustodia)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    if fecha_desde:
        consulta = consulta.filter(InvCustodia.fecha >= fecha_desde)
    if fecha_hasta:
        consulta = consulta.filter(InvCustodia.fecha <= fecha_hasta)
    if usuario_id:
        usuario = get_usuario(db, usuario_id=usuario_id)
        consulta = consulta.filter(InvCustodia.usuario == usuario)
    elif usuario_email:
        usuario = get_usuario_from_email(db, email=usuario_email)
        consulta = consulta.filter(InvCustodia.usuario == usuario)
    return consulta.filter_by(estatus="A").order_by(InvCustodia.id.desc())


def get_inv_custodia(db: Session, inv_custodia_id: int) -> InvCustodia:
    """Consultar un custodia por su id"""
    inv_custodia = db.query(InvCustodia).get(inv_custodia_id)
    if inv_custodia is None:
        raise PWNotExistsError("No existe ese custodia")
    if inv_custodia.estatus != "A":
        raise PWIsDeletedError("No es activo ese custodia, está eliminado")
    return inv_custodia
