"""
Permisos v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError

from ...core.permisos.models import Permiso
from ..modulos.crud import get_modulo
from ..roles.crud import get_rol


def get_permisos(
    db: Session,
    estatus: str = None,
    rol_id: int = None,
    modulo_id: int = None,
) -> Any:
    """Consultar los permisos"""

    # Consultar
    consulta = db.query(Permiso)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por rol
    if rol_id is not None:
        rol = get_rol(db, rol_id)
        consulta = consulta.filter(Permiso.rol == rol)

    # Filtrar por modulo
    if modulo_id is not None:
        modulo = get_modulo(db, modulo_id)
        consulta = consulta.filter(Permiso.modulo == modulo)

    # Entregar
    return consulta.order_by(Permiso.nombre)


def get_permiso(
    db: Session,
    permiso_id: int,
) -> Permiso:
    """Consultar un permiso por su id"""
    permiso = db.query(Permiso).get(permiso_id)
    if permiso is None:
        raise PWNotExistsError("No existe ese permiso")
    if permiso.estatus != "A":
        raise PWIsDeletedError("No es activo ese permiso, está eliminado")
    return permiso
