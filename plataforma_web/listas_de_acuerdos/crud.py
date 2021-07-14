"""
Listas de Acuerdos, CRUD: the four basic operations (create, read, update, and delete) of data storage
"""
from datetime import date
from sqlalchemy.orm import Session

from plataforma_web.autoridades.models import Autoridad
from plataforma_web.distritos.models import Distrito
from plataforma_web.listas_de_acuerdos.models import ListaDeAcuerdo


def get_listas_de_acuerdos(db: Session, autoridad_id: int = None, fecha: date = None, ano: int = None):
    """Consultar listas de acuerdos"""
    listas_de_acuerdos = db.query(ListaDeAcuerdo, Autoridad, Distrito).select_from(ListaDeAcuerdo).join(Autoridad).join(Distrito)
    if autoridad_id:
        listas_de_acuerdos = listas_de_acuerdos.filter(ListaDeAcuerdo.autoridad_id == autoridad_id)
    if fecha:
        listas_de_acuerdos = listas_de_acuerdos.filter(ListaDeAcuerdo.fecha == fecha)
    if ano is not None and 2000 <= ano <= date.today().year:
        listas_de_acuerdos = listas_de_acuerdos.filter(ListaDeAcuerdo.fecha >= date(ano, 1, 1)).filter(ListaDeAcuerdo.fecha <= date(ano, 12, 31))
    return listas_de_acuerdos.filter(ListaDeAcuerdo.estatus == "A").order_by(ListaDeAcuerdo.fecha.desc()).limit(100).all()


def get_lista_de_acuerdo(db: Session, lista_de_acuerdo_id: int):
    """Consultar una lista de acuerdos"""
    return db.query(ListaDeAcuerdo).get(lista_de_acuerdo_id)


def insert_lista_de_acuerdo(db: Session, autoridad_id: int, fecha: date = None, descripcion: str = "", archivo: str = "", url: str = ""):
    """Insertar una lista de acuerdos"""
    autoridad = db.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise ValueError("No existe la autoridad.")
    if autoridad.estatus != "A":
        raise ValueError("No está habilitada la autoridad.")
    if not autoridad.distrito.es_distrito_judicial:
        raise ValueError("No está la autoridad en un distrito judicial.")
    if not autoridad.es_jurisdiccional:
        raise ValueError("No es jurisdiccional la autoridad.")
    if fecha is None:
        fecha = date.today()
    # TODO: Si existe una lista de acuerdo en esa fecha se reemplaza
    if descripcion == "":
        descripcion = "LISTA DE ACUERDOS"
    lista_de_acuerdo = ListaDeAcuerdo(
        autoridad=autoridad,
        fecha=fecha,
        descripcion=descripcion,
        archivo=archivo,
        url=url,
    )
    db.add(lista_de_acuerdo)
    db.commit()
    return lista_de_acuerdo
