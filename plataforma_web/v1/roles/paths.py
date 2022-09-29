"""
Roles v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_roles, get_rol
from .schemas import RolOut, OneRolOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

roles = APIRouter(prefix="/v1/roles", tags=["usuarios"])


@roles.get("", response_model=CustomPage[RolOut])
async def listado_roles(
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de roles"""
    if current_user.permissions.get("ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_roles(
            db=db,
            estatus=estatus,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@roles.get("/{rol_id}", response_model=OneRolOut)
async def detalle_rol(
    rol_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un rol a partir de su id"""
    if current_user.permissions.get("ROLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        rol = get_rol(
            db=db,
            rol_id=rol_id,
        )
    except PWAnyError as error:
        return OneRolOut(success=False, message=str(error))
    return OneRolOut.from_orm(rol)
