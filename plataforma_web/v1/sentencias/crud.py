"""
Sentencias v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from config.settings import SERVIDOR_HUSO_HORARIO
from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWOutOfRangeParamError

from .models import Sentencia
from ..autoridades.crud import get_autoridad, get_autoridad_from_clave
from ..materias_tipos_juicios.crud import get_materia_tipo_juicio


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
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
        consulta = consulta.filter(Sentencia.creado >= desde_dt).filter(Sentencia.creado <= hasta_dt)
    else:
        if creado_desde:
            desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(Sentencia.creado >= desde_dt)
        if creado_hasta:
            hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(SERVIDOR_HUSO_HORARIO)
            consulta = consulta.filter(Sentencia.creado <= hasta_dt)
    if fecha:
        if not date(year=2000, month=1, day=1) <= fecha <= date.today():
            raise PWOutOfRangeParamError("Fecha fuera de rango")
        consulta = consulta.filter_by(sentencia_fecha=fecha)
    else:
        if fecha_desde:
            if not date(year=2000, month=1, day=1) <= fecha_desde <= date.today():
                raise PWOutOfRangeParamError("Fecha fuera de rango")
            consulta = consulta.filter(Sentencia.fecha >= fecha_desde)
        if fecha_hasta:
            if not date(year=2000, month=1, day=1) <= fecha_hasta <= date.today():
                raise PWOutOfRangeParamError("Fecha fuera de rango")
            consulta = consulta.filter(Sentencia.fecha <= fecha_hasta)
    return consulta.filter_by(estatus="A").order_by(Sentencia.id.desc())


def get_sentencia(db: Session, sentencia_id: int) -> Sentencia:
    """Consultar un sentencia por su id"""
    sentencia = db.query(Sentencia).get(sentencia_id)
    if sentencia is None:
        raise PWNotExistsError("No existe esa sentencia")
    if sentencia.estatus != "A":
        raise PWIsDeletedError("No es activa esa sentencia, está eliminada")
    return sentencia
