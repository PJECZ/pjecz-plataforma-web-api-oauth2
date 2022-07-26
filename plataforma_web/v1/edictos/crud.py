"""
Edictos v1, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException, OutOfRangeException

from .models import Edicto
from ..autoridades.crud import get_autoridad


def get_edictos(
    db: Session,
    autoridad_id: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar los edictos activos"""
    consulta = db.query(Edicto)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Edicto.autoridad == autoridad)
    if fecha:
        if not date(year=2000, month=1, day=1) <= fecha <= date.today():
            raise OutOfRangeException("Fecha fuera de rango")
        consulta = consulta.filter_by(fecha=fecha)
    else:
        if fecha_desde:
            if not date(year=2000, month=1, day=1) <= fecha_desde <= date.today():
                raise OutOfRangeException("Fecha fuera de rango")
            consulta = consulta.filter(Edicto.fecha >= fecha_desde)
        if fecha_hasta:
            if not date(year=2000, month=1, day=1) <= fecha_hasta <= date.today():
                raise OutOfRangeException("Fecha fuera de rango")
            consulta = consulta.filter(Edicto.fecha <= fecha_hasta)
    return consulta.filter_by(estatus="A").order_by(Edicto.id)


def get_edicto(db: Session, edicto_id: int) -> Edicto:
    """Consultar un edicto por su id"""
    edicto = db.query(Edicto).get(edicto_id)
    if edicto is None:
        raise NotExistsException("No existe ese edicto")
    if edicto.estatus != "A":
        raise IsDeletedException("No es activo ese edicto, está eliminado")
    return edicto
