"""
REDAM (Registro Estatal de Deudores Alimentarios) v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from .models import Redam
from ..autoridades.crud import get_autoridad
from ..autoridades.models import Autoridad
from ..distritos.crud import get_distrito


def get_redams(
    db: Session,
    autoridad_id: int = None,
    distrito_id: int = None,
    estatus: str = None,
) -> Any:
    """Consultar los deudores"""

    # Consultar
    consulta = db.query(Redam)

    # Filtrar por distrito o autoridad
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id=distrito_id)
        consulta = consulta.join(Autoridad).filter(Autoridad.distrito == distrito)
    elif autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id=autoridad_id)
        consulta = consulta.filter(Redam.autoridad == autoridad)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(Redam.id.desc())


def get_redam(db: Session, redam_id: int) -> Redam:
    """Consultar un deudor por su id"""
    redam = db.query(Redam).get(redam_id)
    if redam is None:
        raise PWNotExistsError("No existe ese deudor")
    if redam.estatus != "A":
        raise PWIsDeletedError("No es activo ese deudor, está eliminado")
    return redam
