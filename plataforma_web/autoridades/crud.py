"""
Autoridades, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from sqlalchemy.orm import Session
from lib.safe_string import safe_clave, safe_string

from plataforma_web.autoridades.models import Autoridad
from plataforma_web.distritos.models import Distrito
from plataforma_web.materias.models import Materia


def get_autoridades(
    db: Session,
    distrito_id: int = None,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
    con_notarias: bool = False,
    para_glosas: bool = False,
):
    """Consultar autoridades"""
    consulta = db.query(Autoridad)
    if distrito_id:
        distrito = db.query(Distrito).get(distrito_id)
        if distrito:
            consulta = consulta.filter(Autoridad.distrito == distrito)
    if materia_id:
        materia = db.query(Materia).get(materia_id)
        if materia:
            consulta = consulta.filter(Autoridad.materia == materia)
    organo_jurisdiccional = safe_string(organo_jurisdiccional)
    if organo_jurisdiccional in Autoridad.ORGANOS_JURISDICCIONALES:
        consulta = consulta.filter_by(organo_jurisdiccional=organo_jurisdiccional)
    if con_notarias is False:
        consulta = consulta.filter_by(es_notaria=False)
    if para_glosas:
        consulta = consulta.filter(Autoridad.organo_jurisdiccional.in_(["PLENO O SALA DEL TSJ", "TRIBUNAL DE CONCILIACION Y ARBITRAJE"]))
    return consulta.filter_by(es_jurisdiccional=True).filter_by(estatus="A").order_by(Autoridad.clave)


"""
    consulta = db.query(Autoridad, Distrito, Materia).select_from(Autoridad).join(Distrito).join(Materia)
"""


def get_autoridad(db: Session, autoridad_id: int):
    """Consultar una autoridad"""
    return db.query(Autoridad).get(autoridad_id)


def get_autoridad_from_clave(db: Session, clave: str):
    """Consultar una autoridad con su clave"""
    try:
        return db.query(Autoridad).filter_by(clave=safe_clave(clave)).first()
    except ValueError as error:
        raise error
