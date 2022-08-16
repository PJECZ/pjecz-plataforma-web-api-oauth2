"""
Sentencias v1, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from lib.exceptions import IsDeletedException, NotExistsException, OutOfRangeException

from .models import Sentencia
from ..autoridades.crud import get_autoridad, get_autoridad_from_clave
from ..materias_tipos_juicios.crud import get_materia_tipo_juicio

HOY = date.today()
ANTIGUA_FECHA = date(year=2000, month=1, day=1)


def get_sentencias(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    materia_tipo_juicio_id: int = None,
) -> Any:
    """Consultar los sentencias activas"""
    consulta = db.query(Sentencia)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Sentencia.autoridad == autoridad)
    elif autoridad_clave:
        autoridad = get_autoridad_from_clave(db, autoridad_clave)
        consulta = consulta.filter(Sentencia.autoridad == autoridad)
    if materia_tipo_juicio_id:
        materia_tipo_juicio = get_materia_tipo_juicio(db, materia_tipo_juicio_id)
        consulta = consulta.filter(Sentencia.materia_tipo_juicio == materia_tipo_juicio)
    if creado:
        if not ANTIGUA_FECHA <= creado <= HOY:
            raise OutOfRangeException("Creado fuera de rango")
        consulta = consulta.filter(func.date(Sentencia.creado) == creado)
    else:
        if creado_desde:
            if not ANTIGUA_FECHA <= creado_desde <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(Sentencia.creado >= creado_desde)
        if creado_hasta:
            if not ANTIGUA_FECHA <= creado_hasta <= HOY:
                raise OutOfRangeException("Creado fuera de rango")
            consulta = consulta.filter(Sentencia.creado <= creado_hasta)
    if fecha:
        if not date(year=2000, month=1, day=1) <= fecha <= date.today():
            raise OutOfRangeException("Fecha fuera de rango")
        consulta = consulta.filter_by(sentencia_fecha=fecha)
    else:
        if fecha_desde:
            if not date(year=2000, month=1, day=1) <= fecha_desde <= date.today():
                raise OutOfRangeException("Fecha fuera de rango")
            consulta = consulta.filter(Sentencia.fecha >= fecha_desde)
        if fecha_hasta:
            if not date(year=2000, month=1, day=1) <= fecha_hasta <= date.today():
                raise OutOfRangeException("Fecha fuera de rango")
            consulta = consulta.filter(Sentencia.fecha <= fecha_hasta)
    return consulta.filter_by(estatus="A").order_by(Sentencia.id.desc())


def get_sentencia(db: Session, sentencia_id: int) -> Sentencia:
    """Consultar un sentencia por su id"""
    sentencia = db.query(Sentencia).get(sentencia_id)
    if sentencia is None:
        raise NotExistsException("No existe esa sentencia")
    if sentencia.estatus != "A":
        raise IsDeletedException("No es activa esa sentencia, está eliminada")
    return sentencia
