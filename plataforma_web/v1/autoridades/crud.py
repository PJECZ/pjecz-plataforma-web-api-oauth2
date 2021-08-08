"""
Autoridades v1.0, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_clave, safe_string
from .models import Autoridad


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
        consulta = consulta.filter_by(distrito_id=distrito_id)
    if materia_id:
        consulta = consulta.filter_by(materia_id=materia_id)
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
    return db.query(Autoridad).get(autoridad_id)


def get_autoridad_from_clave(db: Session, clave: str) -> Autoridad:
    """Consultar una autoridad por su clave"""
    return db.query(Autoridad).filter_by(clave=safe_clave(clave)).first()
