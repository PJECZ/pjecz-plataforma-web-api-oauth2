"""
Listas de Acuerdos, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from datetime import date
from sqlalchemy.orm import Session

from plataforma_web.autoridades.models import Autoridad
from plataforma_web.distritos.models import Distrito
from plataforma_web.listas_de_acuerdos.models import ListaDeAcuerdo
from plataforma_web.listas_de_acuerdos.schemas import ListaDeAcuerdoNew


def get_listas_de_acuerdos(db: Session, autoridad_id: int = None, fecha: date = None, ano: int = None):
    """Consultar listas de acuerdos"""
    consulta = db.query(ListaDeAcuerdo, Autoridad, Distrito).select_from(ListaDeAcuerdo).join(Autoridad).join(Distrito)
    if autoridad_id:
        consulta = consulta.filter(ListaDeAcuerdo.autoridad_id == autoridad_id)
    if fecha:
        consulta = consulta.filter(ListaDeAcuerdo.fecha == fecha)
    if ano is not None and 2000 <= ano <= date.today().year:
        consulta = consulta.filter(ListaDeAcuerdo.fecha >= date(ano, 1, 1)).filter(ListaDeAcuerdo.fecha <= date(ano, 12, 31))
    return consulta.filter(ListaDeAcuerdo.estatus == "A").order_by(ListaDeAcuerdo.fecha.desc()).limit(100).all()


def get_lista_de_acuerdo(db: Session, lista_de_acuerdo_id: int):
    """Consultar una lista de acuerdos"""
    return db.query(ListaDeAcuerdo).get(lista_de_acuerdo_id)


def insert_lista_de_acuerdo(db: Session, lista_de_acuerdo: ListaDeAcuerdoNew):
    """Insertar una lista de acuerdos"""
    autoridad = db.query(Autoridad).get(lista_de_acuerdo.autoridad_id)
    if autoridad is None:
        raise ValueError("No existe la autoridad.")
    if autoridad.estatus != "A":
        raise ValueError("No es activa la autoridad, fue eliminada.")
    if not autoridad.distrito.es_distrito_judicial:
        raise ValueError("No está la autoridad en un distrito judicial.")
    if not autoridad.es_jurisdiccional:
        raise ValueError("No es jurisdiccional la autoridad.")
    if lista_de_acuerdo.fecha is None:
        fecha = date.today()
    else:
        fecha = lista_de_acuerdo.fecha
    # TODO: Si existe una lista de acuerdo en esa fecha se reemplaza
    if lista_de_acuerdo.descripcion == "":
        descripcion = "LISTA DE ACUERDOS"
    else:
        descripcion = lista_de_acuerdo.descripcion
    resultado = ListaDeAcuerdo(
        autoridad=autoridad,
        fecha=fecha,
        descripcion=descripcion,
    )
    db.add(resultado)
    db.commit()
    return resultado
