"""
Distritos v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from plataforma_web.v1.roles.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from .crud import get_distritos, get_distrito
from .schemas import DistritoOut

router = APIRouter()


@router.get("", response_model=LimitOffsetPage[DistritoOut])
async def list_paginate(
    solo_distritos: bool = False,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado paginado de distritos"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_distritos(db, solo_distritos=solo_distritos))


@router.get("/id/{distrito_id}", response_model=DistritoOut)
async def detail(
    distrito_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un distrito a partir de su id"""
    if not current_user.permissions & Permiso.VER_CATALOGOS == Permiso.VER_CATALOGOS:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        distrito = get_distrito(db, distrito_id=distrito_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return DistritoOut(
        id=distrito.id,
        nombre=distrito.nombre,
        nombre_corto=distrito.nombre_corto,
        es_distrito_judicial=distrito.es_distrito_judicial,
    )
