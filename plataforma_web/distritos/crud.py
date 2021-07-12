"""
Distritos, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from sqlalchemy.orm import Session

from plataforma_web.distritos.models import Distrito


def get_distritos(db: Session, solo_distritos: bool = False):
    """Consultar distritos judiciales activos"""
    consulta = db.query(Distrito).filter(Distrito.es_distrito_judicial == True)
    if solo_distritos:
        consulta = consulta.filter(Distrito.nombre.like("Distrito%"))
    return consulta.filter(Distrito.estatus == "A").order_by(Distrito.nombre).all()


def get_distrito(db: Session, distrito_id: int):
    """Consultar un distrito"""
    return db.query(Distrito).get(distrito_id)
