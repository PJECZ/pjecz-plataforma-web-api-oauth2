"""
Autentificaciones
"""
from datetime import datetime
import re
from typing import Optional

from hashids import Hashids
from fastapi.security.api_key import APIKeyHeader
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN
from unidecode import unidecode

from lib.database import get_db
from lib.exceptions import PWAuthenticationError

from .models import Usuario
from .schemas import UsuarioInDB

API_KEY_REGEXP = r"^\w+\.\w+\.\w+$"
X_API_KEY = APIKeyHeader(name="X-Api-Key")


def get_user(
    usuario_id: int,
    db: Session = Depends(get_db),
) -> Optional[UsuarioInDB]:
    """Get user from email"""
    usuario = db.query(Usuario).get(usuario_id)
    if usuario:
        return UsuarioInDB(
            id=usuario.id,
            autoridad_id=usuario.autoridad_id,
            autoridad_clave=usuario.autoridad.clave,
            autoridad_descripcion=usuario.autoridad.descripcion,
            autoridad_descripcion_corta=usuario.autoridad.descripcion_corta,
            distrito_id=usuario.autoridad.distrito_id,
            distrito_nombre=usuario.autoridad.distrito.nombre,
            distrito_nombre_corto=usuario.autoridad.distrito.nombre_corto,
            oficina_id=usuario.oficina_id,
            oficina_clave=usuario.oficina.clave,
            email=usuario.email,
            nombres=usuario.nombres,
            apellido_paterno=usuario.apellido_paterno,
            apellido_materno=usuario.apellido_materno,
            curp=usuario.curp,
            puesto=usuario.puesto,
            telefono=usuario.telefono,
            workspace=usuario.workspace,
            api_key=usuario.api_key,
            api_key_expiracion=usuario.api_key_expiracion,
            username=usuario.email,
            permissions=usuario.permissions,
            hashed_password=usuario.contrasena,
            disabled=usuario.estatus != "A",
        )
    return None


def authenticate_user(
    api_key: str,
    db: Session,
) -> UsuarioInDB:
    """Authenticate user"""

    # Validar con expresion regular
    api_key = unidecode(api_key)
    if re.match(API_KEY_REGEXP, api_key) is None:
        raise PWAuthenticationError("No paso la validacion por expresion regular")

    # Separar el id, el email y la cadena aleatoria del api_key
    api_key_id, api_key_email, api_key_aleatorio = api_key.split(".")

    # Decodificar el ID
    usuario_id = Usuario.decode_id(api_key_id)
    if usuario_id is None:
        raise PWAuthenticationError("No se pudo descifrar el ID")

    # Consultar
    usuario = get_user(usuario_id, db)
    if usuario is None:
        raise PWAuthenticationError("No se encontro el usuario")

    # Validar el api_key
    if usuario.api_key != api_key:
        raise PWAuthenticationError("No es igual la api_key al dato en la base de datos")

    # Validar el email
    if api_key_email != Hashids(salt=usuario.email, min_length=8).encode(1):
        raise PWAuthenticationError("No coincide el correo electronico")

    # Validar el tiempo de expiracion
    if usuario.api_key_expiracion < datetime.now():
        raise PWAuthenticationError("No vigente porque ya expiro")

    # Validad que sea activo
    if usuario.disabled:
        raise PWAuthenticationError("No es activo este usuario porque fue eliminado")

    # Entregar
    return usuario


async def get_current_active_user(
    api_key: str = Depends(X_API_KEY),
    db: Session = Depends(get_db),
):
    """Get current active user"""

    # Try-except
    try:
        usuario = authenticate_user(api_key, db)
    except PWAuthenticationError as error:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=str(error)) from error

    # Entregar
    return usuario
