"""
Listas de Acuerdos Acuerdos, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from sqlalchemy.orm import Session

from plataforma_web.listas_de_acuerdos.models import ListaDeAcuerdo
from plataforma_web.listas_de_acuerdos_acuerdos.models import ListaDeAcuerdoAcuerdo


def get_acuerdos(db: Session, lista_de_acuerdo_id: int):
    """Consultar acuerdos de una lista de acuerdos"""
    return db.query(ListaDeAcuerdoAcuerdo, ListaDeAcuerdo).join(ListaDeAcuerdo).filter(ListaDeAcuerdoAcuerdo.lista_de_acuerdo_id == lista_de_acuerdo_id).filter(ListaDeAcuerdoAcuerdo.estatus == "A").order_by(ListaDeAcuerdoAcuerdo.id).limit(100).all()


def get_acuerdo(db: Session, lista_de_acuerdo_acuerdo_id: int):
    """Consultar un acuerdo"""
    return db.query(ListaDeAcuerdoAcuerdo).get(lista_de_acuerdo_acuerdo_id)


def insert_acuerdo(db: Session, lista_de_acuerdo_id: int):
    """Insertar una lista de acuerdos"""
    acuerdo = ListaDeAcuerdoAcuerdo()
    db.add(acuerdo)
    db.commit()
    return acuerdo
