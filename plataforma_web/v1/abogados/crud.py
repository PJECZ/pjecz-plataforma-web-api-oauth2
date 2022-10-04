"""
Abogados v1, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime

from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWOutOfRangeParamError
from lib.safe_string import safe_string

from .models import Abogado


def get_abogados(
    db: Session,
    anio_desde: int = None,
    anio_hasta: int = None,
    estatus: str = None,
    nombre: str = None,
) -> Any:
    """Consultar los abogados"""

    # Consultar
    consulta = db.query(Abogado)

    # Filtrar por año
    if anio_desde is not None:
        if 1925 <= anio_desde <= datetime.now().year:
            consulta = consulta.filter(Abogado.fecha >= date(year=anio_desde, month=1, day=1))
        else:
            raise PWOutOfRangeParamError("Año fuera de rango.")
    if anio_hasta is not None:
        if 1925 <= anio_hasta <= datetime.now().year:
            consulta = consulta.filter(Abogado.fecha <= date(year=anio_hasta, month=12, day=31))
        else:
            raise PWOutOfRangeParamError("Año fuera de rango.")

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por nombre
    if nombre is not None:
        nombre = safe_string(nombre)
        if nombre != "":
            consulta = consulta.filter(Abogado.nombre.contains(nombre))

    # Entregar
    return consulta.order_by(Abogado.id.desc())


def get_abogado(db: Session, abogado_id: int) -> Abogado:
    """Consultar un abogado por su id"""
    abogado = db.query(Abogado).get(abogado_id)
    if abogado is None:
        raise PWNotExistsError("No existe ese abogado")
    if abogado.estatus != "A":
        raise PWIsDeletedError("No es activo ese abogado, está eliminado")
    return abogado
