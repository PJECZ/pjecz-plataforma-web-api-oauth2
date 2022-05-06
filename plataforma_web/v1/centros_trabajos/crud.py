"""
Centros de Trabajo v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_clave
from plataforma_web.v1.distritos.crud import get_distrito
from plataforma_web.v1.domicilios.crud import get_domicilio
from .models import CentroTrabajo


def get_centros_trabajos(
    db: Session,
    distrito_id: int = None,
    domicilio_id: int = None,
) -> Any:
    """Consultar los centros de trabajo activos"""
    consulta = db.query(CentroTrabajo)
    if distrito_id:
        distrito = get_distrito(db, distrito_id=distrito_id)
        consulta = consulta.filter(CentroTrabajo.distrito == distrito)
    if domicilio_id:
        domicilio = get_domicilio(db, domicilio_id=domicilio_id)
        consulta = consulta.filter(CentroTrabajo.domicilio == domicilio)
    return consulta.filter_by(estatus="A").order_by(CentroTrabajo.id)


def get_centro_trabajo(db: Session, centro_trabajo_id: int) -> CentroTrabajo:
    """Consultar un centro de trabajo por su id"""
    centro_trabajo = db.query(CentroTrabajo).get(centro_trabajo_id)
    if centro_trabajo is None:
        raise IndexError("No existe ese centro de trabajo")
    if centro_trabajo.estatus != "A":
        raise ValueError("No es activo ese centro de trabajo, está eliminado")
    return centro_trabajo


def get_centro_trabajo_from_clave(db: Session, clave: str) -> CentroTrabajo:
    """Consultar un centro de trabajo por su id"""
    clave = safe_clave(clave)  # Si no es correcta causa ValueError
    centro_trabajo = db.query(CentroTrabajo).filter_by(clave=clave).first()
    if centro_trabajo is None:
        raise IndexError("No existe ese centro de trabajo")
    if centro_trabajo.estatus != "A":
        raise ValueError("No es activo ese centro de trabajo, está eliminado")
    return centro_trabajo