"""
Autoridades v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException, NotValidException
from lib.safe_string import safe_clave, safe_string

from .models import Autoridad
from ..distritos.crud import get_distrito
from ..materias.crud import get_materia


def get_autoridades(
    db: Session,
    distrito_id: int = None,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
    son_notarias: bool = False,
) -> Any:
    """Consultar las autoridades jurisdiccionales activas"""
    consulta = db.query(Autoridad).filter_by(es_jurisdiccional=True)
    if distrito_id:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter(Autoridad.distrito == distrito)
    if materia_id:
        materia = get_materia(db, materia_id)
        consulta = consulta.filter(Autoridad.materia == materia)
    organo_jurisdiccional = safe_string(organo_jurisdiccional)
    if organo_jurisdiccional in Autoridad.ORGANOS_JURISDICCIONALES:
        consulta = consulta.filter_by(organo_jurisdiccional=organo_jurisdiccional)
    if son_notarias:
        consulta = consulta.filter_by(es_notaria=True)
    else:
        consulta = consulta.filter_by(es_notaria=False)
    return consulta.filter_by(estatus="A").order_by(Autoridad.clave.asc())


def get_autoridad(db: Session, autoridad_id: int) -> Autoridad:
    """Consultar una autoridad por su id"""
    autoridad = db.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise NotExistsException("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise IsDeletedException("No es activa la autoridad, está eliminada")
    return autoridad


def get_autoridad_from_clave(db: Session, autoridad_clave: str) -> Autoridad:
    """Consultar una autoridad por su clave"""
    try:
        clave = safe_clave(autoridad_clave)
    except ValueError as error:
        raise NotValidException("No es válida la clave") from error
    autoridad = db.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise NotExistsException("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise IsDeletedException("No es activa la autoridad, está eliminada")
    return autoridad
