"""
Listas de Acuerdos v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import AlredyExistsError
from lib.safe_string import safe_string
from plataforma_web.v1.autoridades.crud import get_autoridad
from plataforma_web.v1.listas_de_acuerdos.models import ListaDeAcuerdo
from plataforma_web.v1.listas_de_acuerdos.schemas import ListaDeAcuerdoIn

LIMITE_DIAS = 7


def get_listas_de_acuerdos(
    db: Session,
    autoridad_id: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar las listas de acuerdos activas"""
    consulta = db.query(ListaDeAcuerdo)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(ListaDeAcuerdo.autoridad == autoridad)
    if fecha:
        if not date(year=2000, month=1, day=1) <= fecha <= date.today():
            raise ValueError("Fecha fuera de rango")
        consulta = consulta.filter_by(fecha=fecha)
    else:
        if fecha_desde:
            if not date(year=2000, month=1, day=1) <= fecha_desde <= date.today():
                raise ValueError("Fecha fuera de rango")
            consulta = consulta.filter(ListaDeAcuerdo.fecha >= fecha_desde)
        if fecha_hasta:
            if not date(year=2000, month=1, day=1) <= fecha_hasta <= date.today():
                raise ValueError("Fecha fuera de rango")
            consulta = consulta.filter(ListaDeAcuerdo.fecha <= fecha_hasta)
    return consulta.filter_by(estatus="A").order_by(ListaDeAcuerdo.id.desc())


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
