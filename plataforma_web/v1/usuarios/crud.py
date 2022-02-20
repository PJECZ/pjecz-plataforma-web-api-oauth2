"""
Usuarios v1.0, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from plataforma_web.v1.autoridades.crud import get_autoridad, get_autoridad_from_clave
from plataforma_web.v1.oficinas.crud import get_oficina, get_oficina_from_clave
from plataforma_web.v1.usuarios.models import Usuario


def get_usuarios(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
) -> Any:
    """Consultar los usuarios activos"""
    consulta = db.query(Usuario)
    if autoridad_id:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Usuario.autoridad == autoridad)
    elif autoridad_clave:
        autoridad = get_autoridad_from_clave(db, autoridad_clave)
        consulta = consulta.filter(Usuario.autoridad == autoridad)
    if oficina_id:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(Usuario.oficina == oficina)
    elif oficina_clave:
        oficina = get_oficina_from_clave(db, oficina_clave)
        consulta = consulta.filter(Usuario.oficina == oficina)
    return consulta.order_by(Usuario.email)


def get_usuario(db: Session, usuario_id: int) -> Usuario:
    """Consultar un usuario por su id"""
    usuario = db.query(Usuario).get(usuario_id)
    if usuario is None:
        raise IndexError("No existe ese usuario")
    if usuario.estatus != "A":
        raise ValueError("No es activo el usuario, está eliminado")
    return usuario
