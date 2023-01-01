"""
Glosas v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWOutOfRangeParamError

from .models import Glosa
from ..autoridades.crud import get_autoridad, get_autoridad_from_clave


def get_glosas(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    estatus: str = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar las glosas activas"""

    # Consultar
    consulta = db.query(Glosa)

    # Filtar por autoridad
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Glosa.autoridad == autoridad)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_from_clave(db, autoridad_clave)
        consulta = consulta.filter(Glosa.autoridad == autoridad)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por fecha
    if fecha is not None:
        if not date(year=2000, month=1, day=1) <= fecha <= date.today():
            raise PWOutOfRangeParamError("Fecha fuera de rango")
        consulta = consulta.filter_by(fecha=fecha)
    if fecha is None and fecha_desde is not None:
        if not date(year=2000, month=1, day=1) <= fecha_desde <= date.today():
            raise PWOutOfRangeParamError("Fecha fuera de rango")
        consulta = consulta.filter(Glosa.fecha >= fecha_desde)
    if fecha is None and fecha_hasta is not None:
        if not date(year=2000, month=1, day=1) <= fecha_hasta <= date.today():
            raise PWOutOfRangeParamError("Fecha fuera de rango")
        consulta = consulta.filter(Glosa.fecha <= fecha_hasta)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(Glosa.id.desc())


def get_glosa(db: Session, glosa_id: int) -> Glosa:
    """Consultar una glosa por su id"""
    glosa = db.query(Glosa).get(glosa_id)
    if glosa is None:
        raise PWNotExistsError("No existe ese glosa")
    if glosa.estatus != "A":
        raise PWIsDeletedError("No es activo ese glosa, está eliminado")
    return glosa
