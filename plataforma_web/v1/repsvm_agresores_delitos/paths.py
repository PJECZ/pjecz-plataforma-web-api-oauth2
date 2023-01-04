"""
REPSVM Agresores-Delitos v1, rutas (paths)
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

from .crud import get_repsvm_agresores_delitos, get_repsvm_agresor_delito
from .schemas import REPSVMAgresorDelitoOut

repsvm_agresores_delitos = APIRouter(prefix="/v1/repsvm_agresores_delitos", tags=["repsvm"])


@repsvm_agresores_delitos.get("", response_model=CustomPage[REPSVMAgresorDelitoOut])
async def listado_repsvm_agresores_delitos(
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de agresores-delitos"""
    if current_user.permissions.get("REPSVM AGRESORES DELITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_repsvm_agresores_delitos(
            db=db,
            estatus=estatus,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@repsvm_agresores_delitos.get("/{repsvm_agresor_delito_id}", response_model=REPSVMAgresorDelitoOut)
async def detalle_repsvm_agresor_delito(
    repsvm_agresor_delito_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una agresores-delitos a partir de su id"""
    if current_user.permissions.get("REPSVM AGRESORES DELITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        repsvm_agresor_delito = get_repsvm_agresor_delito(db, repsvm_agresor_delito_id=repsvm_agresor_delito_id)
    except PWAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return REPSVMAgresorDelitoOut.from_orm(repsvm_agresor_delito)
