"""
Modulos v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInBD

from plataforma_web.v1.modulos.crud import get_modulos, get_modulo
from plataforma_web.v1.modulos.schemas import ModuloOut

MODULO = "MODULOS"

router = APIRouter()


@router.get("", response_model=LimitOffsetPage[ModuloOut])
async def list_paginate(
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de modulos"""
    if not current_user.can_view(MODULO):
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_modulos(db))


@router.get("/{modulo_id}", response_model=ModuloOut)
async def detail(
    modulo_id: int,
    current_user: UsuarioInBD = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una modulo a partir de su id"""
    if not current_user.can_view(MODULO):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        modulo = get_modulo(db, modulo_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return ModuloOut.from_orm(modulo)
