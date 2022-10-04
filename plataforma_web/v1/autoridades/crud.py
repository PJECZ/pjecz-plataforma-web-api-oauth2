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
    estatus: str = None,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
) -> Any:
    """Consultar las autoridades jurisdiccionales"""

    # Consultar
    consulta = db.query(Autoridad).filter_by(es_jurisdiccional=True)

    # Filtrar por distrito
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter(Autoridad.distrito == distrito)

    # Filtrar por es_jurisdiccional
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)

    # Filtrar por es_notaria
    if es_notaria is not None:
        consulta = consulta.filter_by(es_notaria=es_notaria)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por materia
    if materia_id is not None:
        materia = get_materia(db, materia_id)
        consulta = consulta.filter(Autoridad.materia == materia)

    # Filtrar por organo_jurisdiccional
    if organo_jurisdiccional is not None:
        organo_jurisdiccional = safe_string(organo_jurisdiccional)
        if organo_jurisdiccional in Autoridad.ORGANOS_JURISDICCIONALES:
            consulta = consulta.filter_by(organo_jurisdiccional=organo_jurisdiccional)

    # Entregar
    return consulta.order_by(Autoridad.clave)


def get_autoridad(
    db: Session,
    autoridad_id: int,
) -> Autoridad:
    """Consultar una autoridad por su id"""
    autoridad = db.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise PWNotExistsError("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise PWIsDeletedError("No es activa la autoridad, está eliminada")
    return autoridad


def get_autoridad_from_clave(
    db: Session,
    autoridad_clave: str,
) -> Autoridad:
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
