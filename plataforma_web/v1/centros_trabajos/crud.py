"""
Centros de Trabajo v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWNotValidParamError
from lib.safe_string import safe_clave

from .models import CentroTrabajo
from ..distritos.crud import get_distrito
from ..domicilios.crud import get_domicilio


def get_centros_trabajos(
    db: Session,
    distrito_id: int = None,
    domicilio_id: int = None,
    estatus: str = None,
) -> Any:
    """Consultar los centros de trabajo activos"""
    consulta = db.query(CentroTrabajo)
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id=distrito_id)
        consulta = consulta.filter(CentroTrabajo.distrito == distrito)
    if domicilio_id is not None:
        domicilio = get_domicilio(db, domicilio_id=domicilio_id)
        consulta = consulta.filter(CentroTrabajo.domicilio == domicilio)
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)
    return consulta.order_by(CentroTrabajo.id.desc())


def get_centro_trabajo(
    db: Session,
    centro_trabajo_id: int,
) -> CentroTrabajo:
    """Consultar un centro de trabajo por su id"""
    centro_trabajo = db.query(CentroTrabajo).get(centro_trabajo_id)
    if centro_trabajo is None:
        raise PWNotExistsError("No existe ese centro de trabajo")
    if centro_trabajo.estatus != "A":
        raise PWIsDeletedError("No es activo ese centro de trabajo, está eliminado")
    return centro_trabajo


def get_centro_trabajo_from_clave(
    db: Session,
    centro_trabajo_clave: str,
) -> CentroTrabajo:
    """Consultar un centro de trabajo por su id"""
    try:
        clave = safe_clave(centro_trabajo_clave)
    except ValueError as error:
        raise PWNotValidParamError("No es válida la clave") from error
    centro_trabajo = db.query(CentroTrabajo).filter_by(clave=clave).first()
    if centro_trabajo is None:
        raise PWNotExistsError("No existe ese centro de trabajo")
    if centro_trabajo.estatus != "A":
        raise PWIsDeletedError("No es activo ese centro de trabajo, está eliminado")
    return centro_trabajo
