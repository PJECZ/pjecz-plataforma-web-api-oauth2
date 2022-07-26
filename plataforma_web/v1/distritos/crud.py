"""
Distritos v1.0, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import IsDeletedException, NotExistsException

from .models import Distrito


def get_distritos(db: Session) -> Any:
    """Consultar los distritos judiciales activos"""
    return db.query(Distrito).filter_by(es_distrito_judicial=True).filter_by(estatus="A").order_by(Distrito.nombre.asc())


def get_distrito(db: Session, distrito_id: int) -> Distrito:
    """Consultar un distrito por su id"""
    distrito = db.query(Distrito).get(distrito_id)
    if distrito is None:
        raise NotExistsException("No existe ese distrito")
    if distrito.estatus != "A":
        raise IsDeletedException("No es activo el distrito, está eliminado")
    return distrito
