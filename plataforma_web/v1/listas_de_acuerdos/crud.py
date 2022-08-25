"""
Listas de Acuerdos v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any, List

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from lib.exceptions import AlredyExistsException, IsDeletedException, NotExistsException, NotValidException, OutOfRangeException
from lib.safe_string import safe_string

from .models import ListaDeAcuerdo
from .schemas import ListaDeAcuerdoIn, ListaDeAcuerdoOut
from ..autoridades.crud import get_autoridad, get_autoridades

LIMITE_DIAS = 7
HOY = date.today()
ANTIGUA_FECHA = date(year=2000, month=1, day=1)


def get_listas_de_acuerdos(
    db: Session,
    autoridad_id: int = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar las listas de acuerdos activas"""
    consulta = db.query(ListaDeAcuerdo)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(ListaDeAcuerdo.autoridad == autoridad)
    if creado:
        if not ANTIGUA_FECHA <= creado <= HOY:
            raise OutOfRangeException("Creado fuera de rango")
        consulta = consulta.filter(func.date(ListaDeAcuerdo.creado) == creado)
    else:
        if creado_desde:
            if not ANTIGUA_FECHA <= creado_desde <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(ListaDeAcuerdo.creado >= creado_desde)
        if creado_hasta:
            if not ANTIGUA_FECHA <= creado_hasta <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(ListaDeAcuerdo.creado <= creado_hasta)
    if fecha:
        if not ANTIGUA_FECHA <= fecha <= HOY:
            raise OutOfRangeException("Fecha fuera de rango")
        consulta = consulta.filter_by(fecha=fecha)
    else:
        if fecha_desde:
            if not ANTIGUA_FECHA <= fecha_desde <= HOY:
                raise OutOfRangeException("Fecha fuera de rango")
            consulta = consulta.filter(ListaDeAcuerdo.fecha >= fecha_desde)
        if fecha_hasta:
            if not ANTIGUA_FECHA <= fecha_hasta <= HOY:
                raise OutOfRangeException("Fecha fuera de rango")
            consulta = consulta.filter(ListaDeAcuerdo.fecha <= fecha_hasta)
    return consulta.filter_by(estatus="A").order_by(ListaDeAcuerdo.id.desc())


def get_lista_de_acuerdo(
    db: Session,
    lista_de_acuerdo_id: int,
) -> ListaDeAcuerdo:
    """Consultar una lista de acuerdo por su id"""
    lista_de_acuerdo = db.query(ListaDeAcuerdo).get(lista_de_acuerdo_id)
    if lista_de_acuerdo is None:
        raise NotExistsException("No exite esa lista de acuerdos")
    if lista_de_acuerdo.estatus != "A":
        raise IsDeletedException("No es activa la lista de acuerdos, fue eliminada")
    return lista_de_acuerdo


def insert_lista_de_acuerdo(
    db: Session,
    lista_de_acuerdo: ListaDeAcuerdoIn,
) -> ListaDeAcuerdo:
    """Insertar una lista de acuerdos"""
    # Validar autoridad
    autoridad = get_autoridad(db, lista_de_acuerdo.autoridad_id)
    if not autoridad.distrito.es_distrito_judicial:
        raise NotValidException("No está la autoridad en un distrito judicial")
    if not autoridad.es_jurisdiccional:
        raise NotValidException("No es jurisdiccional la autoridad")
    # Validar fecha
    hoy_dt = datetime(year=HOY.year, month=HOY.month, day=HOY.day)
    limite_dt = hoy_dt + timedelta(days=-LIMITE_DIAS)
    if lista_de_acuerdo.fecha is None:
        fecha = HOY
    else:
        fecha = lista_de_acuerdo.fecha
        if not limite_dt <= datetime(year=fecha.year, month=fecha.month, day=fecha.day) <= hoy_dt:
            raise OutOfRangeException("Fecha fuera de rango")
    # Si ya existe una lista de acuerdos con esa fecha, se aborta
    existe_esa_lista = db.query(ListaDeAcuerdo).filter_by(autoridad_id=autoridad.id).filter_by(fecha=fecha).filter_by(estatus="A").first()
    if existe_esa_lista:
        raise AlredyExistsException("No se permite otra lista de acuerdos para la autoridad y fechas dadas")
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


def get_listas_de_acuerdos_sintetizar_por_creado(
    db: Session,
    creado: date = None,
    distrito_id: int = None,
) -> List:
    """Consultar las listas de acuerdos por distrito"""

    # Si no se da creado, se toma el día de hoy
    if creado is None:
        creado = HOY

    # Consultar las autoridades del distrito
    autoridades = get_autoridades(
        db=db,
        distrito_id=distrito_id,
        es_jurisdiccional=True,
        es_notaria=False,
    ).all()

    # Consultar las listas de acuerdos de las autoridades
    listas_de_acuerdos = []
    for autoridad in autoridades:
        existentes = get_listas_de_acuerdos(db=db, autoridad_id=autoridad.id, creado=creado).all()
        if existentes:
            # Registros existentes
            for lista_de_acuerdo in existentes:
                listas_de_acuerdos.append(ListaDeAcuerdoOut.from_orm(lista_de_acuerdo))
        else:
            # Registro INEXISTENTE
            listas_de_acuerdos.append(
                ListaDeAcuerdoOut(
                    id=0,
                    autoridad_id=autoridad.id,
                    autoridad_descripcion=autoridad.descripcion,
                    autoridad_descripcion_corta=autoridad.descripcion_corta,
                    autoridad_clave=autoridad.clave,
                    distrito_id=autoridad.distrito_id,
                    distrito_nombre=autoridad.distrito.nombre,
                    distrito_nombre_corto=autoridad.distrito.nombre_corto,
                    descripcion="ND",
                    fecha=creado,
                    archivo="",
                    url="",
                    creado=datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0),
                )
            )

    # Entregar lista
    return listas_de_acuerdos
