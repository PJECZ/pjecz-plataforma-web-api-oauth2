"""
Oficinas v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException
from lib.safe_string import safe_string

from .models import Oficina
from ..distritos.crud import get_distrito
from ..domicilios.crud import get_domicilio


def get_oficinas(
    db: Session,
    distrito_id: int = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = False,
) -> Any:
    """Consultar los oficina activos"""
    consulta = db.query(Oficina)
    if distrito_id:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter(Oficina.distrito == distrito)
    if domicilio_id:
        domicilio = get_domicilio(db, domicilio_id)
        consulta = consulta.filter(Oficina.domicilio == domicilio)
    if es_jurisdiccional is True:
        consulta = consulta.filter_by(es_jurisdiccional=True)
    return consulta.filter_by(estatus="A").order_by(Oficina.clave.asc())


def get_oficina(db: Session, oficina_id: int) -> Oficina:
    """Consultar una oficina por su id"""
    oficina = db.query(Oficina).get(oficina_id)
    if oficina is None:
        raise NotExistsException("No existe ese oficina")
    if oficina.estatus != "A":
        raise IsDeletedException("No es activa ese oficina, está eliminada")
    return oficina


def get_oficina_from_clave(db: Session, oficina_clave: str) -> Oficina:
    """Consultar una oficina por su clave"""
    clave = safe_string(oficina_clave)
    oficina = db.query(Oficina).filter_by(clave=clave).first()
    if oficina is None:
        raise NotExistsException("No existe ese oficina")
    if oficina.estatus != "A":
        raise IsDeletedException("No es activa ese oficina, está eliminada")
    return oficina
