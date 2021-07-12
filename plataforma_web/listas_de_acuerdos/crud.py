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
