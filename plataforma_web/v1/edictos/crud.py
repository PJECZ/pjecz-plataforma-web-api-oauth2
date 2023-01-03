"""
Edictos v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session
import pytz

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from ...core.edictos.models import Edicto
from ..autoridades.crud import get_autoridad, get_autoridad_from_clave


def get_edictos(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estatus: str = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar los edictos"""

    # Zona horaria
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(Edicto)

    # Filtrar por autoridad
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Edicto.autoridad == autoridad)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_from_clave(db, autoridad_clave)
        consulta = consulta.filter(Edicto.autoridad == autoridad)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(Edicto.creado >= desde_dt).filter(Edicto.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(Edicto.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(Edicto.creado <= hasta_dt)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por fecha
    if fecha is not None:
        consulta = consulta.filter_by(fecha=fecha)
    else:
        if fecha_desde:
            consulta = consulta.filter(Edicto.fecha >= fecha_desde)
        if fecha_hasta:
            consulta = consulta.filter(Edicto.fecha <= fecha_hasta)

    # Entregar
    return consulta.order_by(Edicto.id.desc())


def get_edicto(db: Session, edicto_id: int) -> Edicto:
    """Consultar un edicto por su id"""
    edicto = db.query(Edicto).get(edicto_id)
    if edicto is None:
        raise PWNotExistsError("No existe ese edicto")
    if edicto.estatus != "A":
        raise PWIsDeletedError("No es activo ese edicto, está eliminado")
    return edicto
