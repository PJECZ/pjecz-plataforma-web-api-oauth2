"""
Usuarios Roles v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios_roles.crud import get_usuarios_roles, get_usuario_rol
from plataforma_web.v1.usuarios_roles.schemas import UsuarioRolOut
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

usuarios_roles = APIRouter(prefix="/v1/usuarios_roles", tags=["usuarios"])


@usuarios_roles.get("", response_model=LimitOffsetPage[UsuarioRolOut])
async def listado_usuarios_roles(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios_roles"""
    if not current_user.can_view("USUARIOS ROLES"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_usuarios_roles(db))


@usuarios_roles.get("/{usuario_rol_id}", response_model=UsuarioRolOut)
async def detalle_usuario_rol(
    usuario_rol_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una usuario_rol a partir de su id"""
    if not current_user.can_view("USUARIOS ROLES"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario_rol = get_usuario_rol(db, usuario_rol_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return UsuarioRolOut.from_orm(usuario_rol)
