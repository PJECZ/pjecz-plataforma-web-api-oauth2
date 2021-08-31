"""
Usuarios v1.0, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from plataforma_web.v1.autoridades.crud import get_autoridad
from plataforma_web.v1.roles.crud import get_rol
from plataforma_web.v1.usuarios.models import Usuario


def get_usuarios(
    db: Session,
    autoridad_id: int = None,
    rol_id: int = None,
) -> Any:
    """Consultar los usuarios activos"""
    consulta = db.query(Usuario)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Usuario.autoridad == autoridad)
    if rol_id:
        rol = get_rol(db, rol_id)
        consulta = consulta.filter(Usuario.rol == rol)
    return consulta.order_by(Usuario.email)


def get_usuario(db: Session, usuario_id: int) -> Usuario:
    """Consultar un usuario por su id"""
    usuario = db.query(Usuario).get(usuario_id)
    if usuario is None:
        raise IndexError("No existe ese usuario")
    if usuario.estatus != "A":
        raise ValueError("No es activo el usuario, está eliminado")
    return usuario
