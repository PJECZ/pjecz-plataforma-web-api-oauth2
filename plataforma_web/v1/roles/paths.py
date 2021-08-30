"""
Roles v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from plataforma_web.v1.roles.crud import get_roles, get_rol
from plataforma_web.v1.roles.schemas import RolOut

v1_roles = APIRouter(prefix="/v1/roles", tags=["roles"])


@v1_roles.get("", response_model=LimitOffsetPage[RolOut])
async def listado_roles(
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado paginado de roles"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_roles(db))


@v1_roles.get("/id/{rol_id}", response_model=RolOut)
async def detalle_rol(
    rol_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un rol a partir de su id"""
    if not current_user.permissions & Permiso.VER_CUENTAS == Permiso.VER_CUENTAS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        rol = get_rol(db, rol_id=rol_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return RolOut.from_orm(rol)
