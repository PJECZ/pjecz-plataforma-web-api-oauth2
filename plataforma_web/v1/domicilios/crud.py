"""
Domicilios v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWNotValidParamError
from lib.safe_string import safe_string

from ...core.distritos.models import Domicilio


def get_domicilios(
    db: Session,
    estatus: str = None,
) -> Any:
    """Consultar los domicilios"""

    # Consultar
    consulta = db.query(Domicilio)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(Domicilio.edificio)


def get_domicilio(
    db: Session,
    domicilio_id: int,
) -> Domicilio:
    """Consultar un domicilio por su id"""
    domicilio = db.query(Domicilio).get(domicilio_id)
    if domicilio is None:
        raise PWNotExistsError("No existe ese domicilio")
    if domicilio.estatus != "A":
        raise PWIsDeletedError("No es activo ese domicilio, está eliminado")
    return domicilio


def get_domicilio_from_edificio(
    db: Session,
    domicilio_edificio: str,
) -> Domicilio:
    """Consultar un domicilio por su edificio"""
    try:
        edificio = safe_string(domicilio_edificio, do_unidecode=False)
    except ValueError as error:
        raise PWNotValidParamError("No es válida el edificio") from error
    domicilio = db.query(Domicilio).filter_by(edificio=edificio).first()
    if domicilio is None:
        raise PWNotExistsError("No existe ese domicilio")
    if domicilio.estatus != "A":
        raise PWIsDeletedError("No es activa ese domicilio, está eliminada")
    return domicilio
