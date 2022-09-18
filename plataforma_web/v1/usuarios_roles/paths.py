"""
Usuarios Roles v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_usuarios_roles, get_usuario_rol
from .schemas import UsuarioRolOut, OneUsuarioRolOut
from ..usuarios.authentications import get_current_active_user
from ..permisos.models import Permiso
from ..usuarios.schemas import UsuarioInDB

usuarios_roles = APIRouter(prefix="/v1/usuarios_roles", tags=["usuarios"])


@usuarios_roles.get("", response_model=CustomPage[UsuarioRolOut])
async def listado_usuarios_roles(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios_roles"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_usuarios_roles(db)
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@usuarios_roles.get("/{usuario_rol_id}", response_model=OneUsuarioRolOut)
async def detalle_usuario_rol(
    usuario_rol_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una usuario_rol a partir de su id"""
    if current_user.permissions.get("USUARIOS ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario_rol = get_usuario_rol(
            db,
            usuario_rol_id=usuario_rol_id,
        )
    except PWAnyError as error:
        return OneUsuarioRolOut(success=False, message=str(error))
    return OneUsuarioRolOut.from_orm(usuario_rol)
