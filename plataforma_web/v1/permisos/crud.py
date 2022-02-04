"""
Permisos v1, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.modulos.crud import get_modulo
from plataforma_web.v1.roles.crud import get_rol


def get_permisos(
    db: Session,
    rol_id: int = None,
    modulo_id: int = None,
) -> Any:
    """Consultar los permisos activos"""
    consulta = db.query(Permiso)
    if rol_id:
        rol = get_rol(db, rol_id)
        consulta = consulta.filter(Permiso.rol == rol)
    if modulo_id:
        modulo = get_modulo(db, modulo_id)
        consulta = consulta.filter(Permiso.modulo == modulo)
    return consulta.filter_by(estatus="A").order_by(Permiso.nombre)


def get_permiso(db: Session, permiso_id: int) -> Permiso:
    """Consultar un permiso por su id"""
    permiso = db.query(Permiso).get(permiso_id)
    if permiso is None:
        raise IndexError("No existe ese permiso")
    if permiso.estatus != "A":
        raise ValueError("No es activo ese permiso, está eliminado")
    return permiso
