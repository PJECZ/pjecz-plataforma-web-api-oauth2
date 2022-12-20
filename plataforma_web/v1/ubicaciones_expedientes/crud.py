"""
Ubicaciones Expedientes v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError
from lib.safe_string import safe_expediente

from .models import UbicacionExpediente
from ..autoridades.crud import get_autoridad, get_autoridad_from_clave


def get_ubicaciones_expedientes(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    expediente: str = None,
) -> Any:
    """Consultar las ubicaciones de expedientes activos"""

    # Consultar
    consulta = db.query(UbicacionExpediente)

    # Filtar por autoridad
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(UbicacionExpediente.autoridad == autoridad)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_from_clave(db, autoridad_clave)
        consulta = consulta.filter(UbicacionExpediente.autoridad == autoridad)

    # Filtrar por expediente
    if expediente is not None:
        expediente = safe_expediente(expediente)
        if expediente != "":
            consulta = consulta.filter_by(expediente=expediente)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(UbicacionExpediente.id.desc())


def get_ubicacion_expediente(db: Session, ubicacion_expediente_id: int) -> UbicacionExpediente:
    """Consultar una ubicacion de expediente por su id"""
    ubicacion_expediente = db.query(UbicacionExpediente).get(ubicacion_expediente_id)
    if ubicacion_expediente is None:
        raise PWNotExistsError("No existe ese ubicacion de expediente")
    if ubicacion_expediente.estatus != "A":
        raise PWIsDeletedError("No es activo ese ubicacion de expediente, está eliminado")
    return ubicacion_expediente
