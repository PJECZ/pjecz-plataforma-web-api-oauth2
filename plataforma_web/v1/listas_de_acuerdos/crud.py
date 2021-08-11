"""
Listas de Acuerdos v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import AlredyExistsError
from lib.safe_string import safe_string
from .models import ListaDeAcuerdo
from .schemas import ListaDeAcuerdoIn
from ..autoridades.crud import get_autoridad, get_autoridad_from_clave

LIMITE_DIAS = 7


def get_listas_de_acuerdos(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    fecha: date = None,
    anio: int = None,
) -> Any:
    """Consultar las listas de acuerdos activas"""
    consulta = db.query(ListaDeAcuerdo)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(ListaDeAcuerdo.autoridad == autoridad)
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
    """Consultar una lista de acuerdo por su id"""
    lista_de_acuerdo = db.query(ListaDeAcuerdo).get(lista_de_acuerdo_id)
    if lista_de_acuerdo is None:
        raise IndexError("No exite esa lista de acuerdos")
    if lista_de_acuerdo.estatus != "A":
        raise ValueError("No es activa la lista de acuerdos, fue eliminada")
    return lista_de_acuerdo


def insert_lista_de_acuerdo(db: Session, lista_de_acuerdo: ListaDeAcuerdoIn) -> ListaDeAcuerdo:
    """Insertar una lista de acuerdos"""
    # Validar autoridad
    autoridad = get_autoridad(db, lista_de_acuerdo.autoridad_id)
    if not autoridad.distrito.es_distrito_judicial:
        raise ValueError("No está la autoridad en un distrito judicial")
    if not autoridad.es_jurisdiccional:
        raise ValueError("No es jurisdiccional la autoridad")
    # Validar fecha
    hoy = date.today()
    hoy_dt = datetime(year=hoy.year, month=hoy.month, day=hoy.day)
    limite_dt = hoy_dt + timedelta(days=-LIMITE_DIAS)
    if lista_de_acuerdo.fecha is None:
        fecha = hoy
    else:
        fecha = lista_de_acuerdo.fecha
        if not limite_dt <= datetime(year=fecha.year, month=fecha.month, day=fecha.day) <= hoy_dt:
            raise ValueError("Fecha fuera de rango")
    # Si ya existe una lista de acuerdos con esa fecha, se aborta
    existe_esa_lista = db.query(ListaDeAcuerdo).filter_by(autoridad_id=autoridad.id).filter_by(fecha=fecha).filter_by(estatus="A").first()
    if existe_esa_lista:
        raise AlredyExistsError("No se permite otra lista de acuerdos para la autoridad y fechas dadas")
    # Validar descripcion
    if lista_de_acuerdo.descripcion == "":
        descripcion = "LISTA DE ACUERDOS"
    else:
        descripcion = safe_string(lista_de_acuerdo.descripcion)
    # Insertar
    resultado = ListaDeAcuerdo(
        autoridad=autoridad,
        fecha=fecha,
        descripcion=descripcion,
    )
    db.add(resultado)
    db.commit()
    return resultado
