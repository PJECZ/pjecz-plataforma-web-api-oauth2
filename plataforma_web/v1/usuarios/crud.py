"""
Usuarios v1.0, CRUD (create, read, update, and delete)
"""
import re
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import PWIsDeletedError, PWNotExistsError, PWNotValidParamError
from lib.safe_string import EMAIL_REGEXP, safe_string

from .models import Usuario
from ..autoridades.crud import get_autoridad, get_autoridad_from_clave
from ..oficinas.crud import get_oficina, get_oficina_from_clave


def get_usuarios(
    db: Session,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    estatus: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
    workspace: str = None,
) -> Any:
    """Consultar los usuarios"""

    # Consultar
    consulta = db.query(Usuario)

    # Filtrar por autoridad
    if autoridad_id is not None:
        autoridad = get_autoridad(db, autoridad_id)
        consulta = consulta.filter(Usuario.autoridad == autoridad)
    elif autoridad_clave is not None:
        autoridad = get_autoridad_from_clave(db, autoridad_clave)
        consulta = consulta.filter(Usuario.autoridad == autoridad)

    # Filtrar por estatus
    if estatus is None:
        consulta = consulta.filter_by(estatus="A")  # Si no se da el estatus, solo activos
    else:
        consulta = consulta.filter_by(estatus=estatus)

    # Filtrar por oficina
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(Usuario.oficina == oficina)
    elif oficina_clave is not None:
        oficina = get_oficina_from_clave(db, oficina_clave)
        consulta = consulta.filter(Usuario.oficina == oficina)

    # Filtrar por workspace
    if workspace is not None:
        workspace = safe_string(workspace)
        if workspace in Usuario.WORKSPACES:
            consulta = consulta.filter_by(workspace=workspace)

    # Entregar
    return consulta.order_by(Usuario.email)


def get_usuario(
    db: Session,
    usuario_id: int,
) -> Usuario:
    """Consultar un usuario por su id"""
    usuario = db.query(Usuario).get(usuario_id)
    if usuario is None:
        raise PWNotExistsError("No existe ese usuario")
    if usuario.estatus != "A":
        raise PWIsDeletedError("No es activo el usuario, está eliminado")
    return usuario


def get_usuario_from_email(
    db: Session,
    email: str,
) -> Usuario:
    """Consultar un usuario por su email"""
    if re.match(EMAIL_REGEXP, email) is None:
        raise PWNotValidParamError("El e-mail es incorrecto")
    usuario = db.query(Usuario).filter_by(email=email).first()
    if usuario is None:
        raise PWNotExistsError("No existe ese usuario")
    if usuario.estatus != "A":
        raise PWIsDeletedError("No es activo el usuario, está eliminado")
    return usuario
