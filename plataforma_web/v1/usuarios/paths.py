"""
Usuarios v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.crud import get_usuarios, get_usuario
from plataforma_web.v1.usuarios.schemas import UsuarioOut, UsuarioInBD

usuarios = APIRouter(prefix="/v1/usuarios", tags=["usuarios"])


@usuarios.get("", response_model=LimitOffsetPage[UsuarioOut])
async def listado_usuarios(
    autoridad_id: int = None,
    rol_id: int = None,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_usuarios(db, autoridad_id=autoridad_id, rol_id=rol_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@usuarios.get("/{usuario_id}", response_model=UsuarioOut)
async def detalle_usuario(
    usuario_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un usuario a partir de su id"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        usuario = get_usuario(db, usuario_id=usuario_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return UsuarioOut.from_orm(usuario)
