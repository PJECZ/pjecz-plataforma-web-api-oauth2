"""
REPSVM Agresores v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

from .crud import get_repsvm_agresores, get_repsvm_agresor
from .schemas import REPSVMAgresorOut

repsvm_agresores = APIRouter(prefix="/v1/repsvm_agresores", tags=["repsvm"])


@repsvm_agresores.get("", response_model=CustomPage[REPSVMAgresorOut])
async def listado_repsvm_agresores(
    distrito_id: int = None,
    estatus: str = None,
    nombre: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de agresores"""
    if current_user.permissions.get("REPSVM AGRESORES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_repsvm_agresores(
            db=db,
            distrito_id=distrito_id,
            estatus=estatus,
            nombre=nombre,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@repsvm_agresores.get("/{repsvm_agresor_id}", response_model=REPSVMAgresorOut)
async def detalle_repsvm_agresor(
    repsvm_agresor_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una agresores a partir de su id"""
    if current_user.permissions.get("REPSVM AGRESORES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        repsvm_agresor = get_repsvm_agresor(db, repsvm_agresor_id=repsvm_agresor_id)
    except PWAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return REPSVMAgresorOut.from_orm(repsvm_agresor)
