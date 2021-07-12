"""
Listas de Acuerdos Acuerdos, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from sqlalchemy.orm import Session

from plataforma_web.listas_de_acuerdos.models import ListaDeAcuerdo
from plataforma_web.listas_de_acuerdos_acuerdos.models import ListaDeAcuerdoAcuerdo


def get_listas_de_acuerdos_acuerdos(db: Session, lista_de_acuerdo_id: int):
    """Consultar listas_de_acuerdos_acuerdos"""
    return db.query(ListaDeAcuerdoAcuerdo, ListaDeAcuerdo).join(ListaDeAcuerdo).filter(ListaDeAcuerdoAcuerdo.lista_de_acuerdo_id == lista_de_acuerdo_id).filter(ListaDeAcuerdoAcuerdo.estatus == "A").order_by(ListaDeAcuerdoAcuerdo.id).limit(100).all()


def get_lista_de_acuerdo_acuerdo(db: Session, lista_de_acuerdo_acuerdo_id: int):
    """Consultar un lista_de_acuerdo_acuerdo"""
    return db.query(ListaDeAcuerdoAcuerdo).get(lista_de_acuerdo_acuerdo_id)
