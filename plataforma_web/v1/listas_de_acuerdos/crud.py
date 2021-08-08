"""
Listas de Acuerdos v1, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from .models import ListaDeAcuerdo
from ..autoridades.crud import get_autoridad, get_autoridad_from_clave


def get_listas_de_acuerdos(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    fecha: date = None,
    anio: int = None,
) -> Any:
    """ Consultar las listas de acuerdos activas """
    consulta = db.query(ListaDeAcuerdo)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter_by(autoridad_id=autoridad.id)
    elif autoridad_clave:
        autoridad = get_autoridad_from_clave(db, autoridad_clave)
        consulta = consulta.filter(ListaDeAcuerdo.autoridad == autoridad)
    if fecha:
        if not date(year=2000, month=1, day=1) <= fecha <= date.today():
            raise ValueError("Fecha fuera de rango")
        consulta = consulta.filter_by(fecha=fecha)
    if anio:
        if not 2000 <= anio <= date.today().year:
            raise ValueError("Año fuera de rango")
        consulta = consulta.filter(ListaDeAcuerdo.fecha >= date(anio, 1, 1))
        consulta = consulta.filter(ListaDeAcuerdo.fecha <= date(anio, 12, 31))
    return consulta.filter_by(estatus="A").order_by(ListaDeAcuerdo.fecha.desc())


def get_lista_de_acuerdo(db: Session, lista_de_acuerdo_id: int) -> ListaDeAcuerdo:
    """ Consultar una lista de acuerdo por su id """
    lista_de_acuerdo = db.query(ListaDeAcuerdo).get(lista_de_acuerdo_id)
    if lista_de_acuerdo is None:
        raise IndexError
    return lista_de_acuerdo
