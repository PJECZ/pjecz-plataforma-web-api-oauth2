"""
REPSVM Delitos v1, rutas (paths)
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

from .crud import get_repsvm_delitos, get_repsvm_delito
from .schemas import REPSVMDelitoOut

repsvm_delitos = APIRouter(prefix="/v1/repsvm_delitos", tags=["repsvm"])


@repsvm_delitos.get("", response_model=CustomPage[REPSVMDelitoOut])
async def listado_repsvm_delitos(
    estatus: str = None,
    nombre: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de delitos"""
    if current_user.permissions.get("REPSVM DELITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_repsvm_delitos(
            db=db,
            estatus=estatus,
            nombre=nombre,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@repsvm_delitos.get("/{repsvm_delito_id}", response_model=REPSVMDelitoOut)
async def detalle_repsvm_delito(
    repsvm_delito_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una delitos a partir de su id"""
    if current_user.permissions.get("REPSVM DELITOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        repsvm_delito = get_repsvm_delito(db, repsvm_delito_id=repsvm_delito_id)
    except PWAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return REPSVMDelitoOut.from_orm(repsvm_delito)
