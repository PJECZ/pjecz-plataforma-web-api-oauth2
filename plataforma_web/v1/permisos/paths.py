"""
Permisos v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.permisos.crud import get_permisos, get_permiso
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.permisos.schemas import PermisoOut
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

permisos = APIRouter(prefix="/v1/permisos", tags=["usuarios"])


@permisos.get("", response_model=LimitOffsetPage[PermisoOut])
async def list_paginate(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de permisos"""
    if "PERMISOS" not in current_user.permissions or current_user.permissions["PERMISOS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_permisos(db))


@permisos.get("/{permiso_id}", response_model=PermisoOut)
async def detail(
    permiso_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una permiso a partir de su id"""
    if "PERMISOS" not in current_user.permissions or current_user.permissions["PERMISOS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        permiso = get_permiso(db, permiso_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return PermisoOut.from_orm(permiso)
