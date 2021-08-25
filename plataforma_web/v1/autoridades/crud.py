"""
Autoridades v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_clave, safe_string
from .models import Autoridad
from ..distritos.crud import get_distrito
from ..materias.crud import get_materia


def get_autoridades(
    db: Session,
    distrito_id: int = None,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
    con_notarias: bool = False,
    para_glosas: bool = False,
) -> Any:
    """Consultar las autoridades activas"""
    consulta = db.query(Autoridad)
    if distrito_id:
        distrito = get_distrito(db, distrito_id)  # Si no se encuentra provoca una excepción
        consulta = consulta.filter(Autoridad.distrito == distrito)
    if materia_id:
        materia = get_materia(db, materia_id)  # Si no se encuentra provoca una excepción
        consulta = consulta.filter_by(Autoridad.materia == materia)
    organo_jurisdiccional = safe_string(organo_jurisdiccional)
    if organo_jurisdiccional in Autoridad.ORGANOS_JURISDICCIONALES:
        consulta = consulta.filter_by(organo_jurisdiccional=organo_jurisdiccional)
    if con_notarias is False:
        consulta = consulta.filter_by(es_notaria=False)
    if para_glosas:
        consulta = consulta.filter(Autoridad.organo_jurisdiccional.in_(["PLENO O SALA DEL TSJ", "TRIBUNAL DE CONCILIACION Y ARBITRAJE"]))
    return consulta.filter_by(estatus="A").order_by(Autoridad.clave)


def get_autoridad(db: Session, autoridad_id: int) -> Autoridad:
    """Consultar una autoridad por su id"""
    autoridad = db.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise IndexError("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise ValueError("No es activa la autoridad, está eliminada")
    return autoridad


def get_autoridad_from_clave(db: Session, clave: str) -> Autoridad:
    """Consultar una autoridad por su clave"""
    clave = safe_clave(clave)  # Si no es correcta causa ValueError
    autoridad = db.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise IndexError("No existe esa autoridad")
    if autoridad.estatus != "A":
        raise ValueError("No es activa la autoridad, está eliminada")
    return autoridad
