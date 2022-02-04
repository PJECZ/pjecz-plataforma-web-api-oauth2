"""
Roles v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD, UsuarioOut

from plataforma_web.v1.roles.crud import get_roles, get_rol
from plataforma_web.v1.roles.schemas import RolOut
from plataforma_web.v1.usuarios.crud import get_usuarios

MODULO = "ROLES"

roles = APIRouter(prefix="/v1/roles", tags=["roles"])


@roles.get("", response_model=LimitOffsetPage[RolOut])
async def listado_roles(
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de roles"""
    if not current_user.can_view(MODULO):
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_roles(db))


@roles.get("/{rol_id}", response_model=RolOut)
async def detalle_rol(
    rol_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un rol a partir de su id"""
    if not current_user.can_view(MODULO):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        rol = get_rol(db, rol_id=rol_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return RolOut.from_orm(rol)


@roles.get("/{rol_id}/usuarios", response_model=LimitOffsetPage[UsuarioOut])
async def listado_usuarios_de_rol(
    rol_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de usuarios de un rol"""
    if not current_user.can_view(MODULO):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_usuarios(db, rol_id=rol_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)
