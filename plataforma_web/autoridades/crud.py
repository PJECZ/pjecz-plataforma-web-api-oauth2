"""
Autoridades, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from sqlalchemy.orm import Session
from lib.safe_string import safe_string

from plataforma_web.autoridades.models import Autoridad
from plataforma_web.distritos.models import Distrito
from plataforma_web.materias.models import Materia


def get_autoridades(db: Session, distrito_id: int = None, materia_id: int = None, organo_jurisdiccional: str = None, con_notarias: bool = False, para_glosas: bool = False):
    """Consultar autoridades"""
    consulta = db.query(Autoridad, Distrito, Materia).select_from(Autoridad).join(Distrito).join(Materia)
    if distrito_id:
        consulta = consulta.filter(Autoridad.distrito_id == distrito_id)
    if materia_id:
        consulta = consulta.filter(Autoridad.materia_id == materia_id)
    organo_jurisdiccional = safe_string(organo_jurisdiccional)
    if organo_jurisdiccional in Autoridad.ORGANOS_JURISDICCIONALES:
        consulta = consulta.filter(Autoridad.organo_jurisdiccional == organo_jurisdiccional)
    if con_notarias is False:
        consulta = consulta.filter(Autoridad.es_notaria == False)
    if para_glosas:
        consulta = consulta.filter(Autoridad.organo_jurisdiccional.in_(["PLENO O SALA DEL TSJ", "TRIBUNAL DE CONCILIACION Y ARBITRAJE"]))
    return consulta.filter(Autoridad.es_jurisdiccional == True).filter(Autoridad.estatus == "A").order_by(Distrito.nombre, Autoridad.clave).all()


def get_autoridad(db: Session, autoridad_id: int):
    """Consultar una autoridad"""
    return db.query(Autoridad).get(autoridad_id)
