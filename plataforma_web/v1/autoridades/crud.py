"""
Autoridades v1, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWNotValidParamError
from lib.safe_string import safe_clave, safe_string

from .models import Autoridad
from ..distritos.crud import get_distrito
from ..materias.crud import get_materia


def get_autoridades(
    db: Session,
    distrito_id: int = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
) -> Any:
    """Consultar las autoridades jurisdiccionales activas"""
    consulta = db.query(Autoridad).filter_by(es_jurisdiccional=True)
    if distrito_id:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter(Autoridad.distrito == distrito)
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)
    if es_notaria is not None:
        consulta = consulta.filter_by(es_notaria=es_notaria)
    if materia_id:
        materia = get_materia(db, materia_id)
        consulta = consulta.filter(Autoridad.materia == materia)
    if organo_jurisdiccional is not None:
        organo_jurisdiccional = safe_string(organo_jurisdiccional)
        if organo_jurisdiccional in Autoridad.ORGANOS_JURISDICCIONALES:
            consulta = consulta.filter_by(organo_jurisdiccional=organo_jurisdiccional)
    return consulta.filter_by(estatus="A").order_by(Autoridad.clave.asc())


def get_autoridad(db: Session, autoridad_id: int) -> Autoridad:
    """Consultar una autoridad por su id"""
    autoridad = db.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise PWNotExistsError("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise PWIsDeletedError("No es activa la autoridad, está eliminada")
    return autoridad


def get_autoridad_from_clave(db: Session, autoridad_clave: str) -> Autoridad:
    """Consultar una autoridad por su clave"""
    try:
        clave = safe_clave(autoridad_clave)
    except ValueError as error:
        raise PWNotValidParamError("No es válida la clave") from error
    autoridad = db.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise PWNotExistsError("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise PWIsDeletedError("No es activa la autoridad, está eliminada")
    return autoridad
