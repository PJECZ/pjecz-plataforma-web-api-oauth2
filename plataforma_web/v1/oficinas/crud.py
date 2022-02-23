"""
Oficinas v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_string

from plataforma_web.v1.domicilios.crud import get_domicilio
from plataforma_web.v1.oficinas.models import Oficina


def get_oficinas(
    db: Session,
    domicilio_id: int = None,
    es_jurisdiccional: bool = False,
) -> Any:
    """Consultar los oficina activos"""
    consulta = db.query(Oficina)
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
        raise IndexError("No existe ese oficina")
    if oficina.estatus != "A":
        raise ValueError("No es activa ese oficina, está eliminada")
    return oficina


def get_oficina_from_clave(db: Session, oficina_clave: str) -> Oficina:
    """Consultar una oficina por su clave"""
    clave = safe_string(oficina_clave)
    oficina = db.query(Oficina).filter_by(clave=clave).first()
    if oficina is None:
        raise IndexError("No existe ese oficina")
    if oficina.estatus != "A":
        raise ValueError("No es activa ese oficina, está eliminada")
    return oficina
