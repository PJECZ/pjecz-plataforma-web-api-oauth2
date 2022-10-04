"""
Oficinas v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWNotValidParamError
from lib.safe_string import safe_clave

from .models import Oficina
from ..distritos.crud import get_distrito
from ..domicilios.crud import get_domicilio


def get_oficinas(
    db: Session,
    distrito_id: int = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
    estatus: str = None,
) -> Any:
    """Consultar las oficinas"""

    # Consultar
    consulta = db.query(Oficina)

    # Filtrar por distrito
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter(Oficina.distrito == distrito)

    # Filtrar por domicilio
    if domicilio_id is not None:
        domicilio = get_domicilio(db, domicilio_id)
        consulta = consulta.filter(Oficina.domicilio == domicilio)

    # Filtrar por jurisdiccional
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.order_by(Oficina.clave.asc())


def get_oficina(
    db: Session,
    oficina_id: int,
) -> Oficina:
    """Consultar una oficina por su id"""
    oficina = db.query(Oficina).get(oficina_id)
    if oficina is None:
        raise PWNotExistsError("No existe ese oficina")
    if oficina.estatus != "A":
        raise PWIsDeletedError("No es activa ese oficina, está eliminada")
    return oficina


def get_oficina_from_clave(
    db: Session,
    oficina_clave: str,
) -> Oficina:
    """Consultar una oficina por su clave"""
    try:
        clave = safe_clave(oficina_clave)
    except ValueError as error:
        raise PWNotValidParamError("No es válida la clave") from error
    oficina = db.query(Oficina).filter_by(clave=clave).first()
    if oficina is None:
        raise PWNotExistsError("No existe ese oficina")
    if oficina.estatus != "A":
        raise PWIsDeletedError("No es activa ese oficina, está eliminada")
    return oficina
