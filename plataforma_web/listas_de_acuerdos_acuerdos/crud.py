"""
Listas de Acuerdos Acuerdos, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from sqlalchemy.orm import Session

from plataforma_web.autoridades.models import Autoridad
from plataforma_web.distritos.models import Distrito
from plataforma_web.listas_de_acuerdos.models import ListaDeAcuerdo
from plataforma_web.listas_de_acuerdos_acuerdos.models import ListaDeAcuerdoAcuerdo
from plataforma_web.listas_de_acuerdos_acuerdos.schemas import ListaDeAcuerdoAcuerdoNew


def get_acuerdos(db: Session, lista_de_acuerdo_id: int):
    """Consultar acuerdos de una lista de acuerdos"""
    return (
        db.query(ListaDeAcuerdoAcuerdo, ListaDeAcuerdo, Autoridad, Distrito)
        .select_from(ListaDeAcuerdoAcuerdo)
        .join(ListaDeAcuerdo)
        .join(Autoridad)
        .join(Distrito)
        .filter(ListaDeAcuerdoAcuerdo.lista_de_acuerdo_id == lista_de_acuerdo_id)
        .filter(ListaDeAcuerdoAcuerdo.estatus == "A")
        .order_by(ListaDeAcuerdoAcuerdo.id)
        .limit(100)
        .all()
    )


def get_acuerdo(db: Session, lista_de_acuerdo_acuerdo_id: int):
    """Consultar un acuerdo"""
    return db.query(ListaDeAcuerdoAcuerdo).get(lista_de_acuerdo_acuerdo_id)


def insert_acuerdo(db: Session, acuerdo: ListaDeAcuerdoAcuerdoNew):
    """Insertar una lista de acuerdos"""
    lista_de_acuerdo = db.query(ListaDeAcuerdo).get(acuerdo.lista_de_acuerdo_id)
    if lista_de_acuerdo is None:
        raise ValueError("No existe la lista de acuerdos.")
    if lista_de_acuerdo.estatus != "A":
        raise ValueError("No es activa la lista de acuardos, fue eliminada.")
    resultado = ListaDeAcuerdoAcuerdo(
        lista_de_acuerdo=lista_de_acuerdo,
        folio=acuerdo.folio,
        expediente=acuerdo.expediente,
        actor=acuerdo.actor,
        demandado=acuerdo.demandado,
        tipo_acuerdo=acuerdo.tipo_acuerdo,
        tipo_juicio=acuerdo.tipo_juicio,
        referencia=acuerdo.referencia,
    )
    db.add(resultado)
    db.commit()
    return resultado
