"""
REDAM v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_redams, get_redam
from .schemas import RedamOut, OneRedamOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

redams = APIRouter(prefix="/v1/redams", tags=["redam"])


@redams.get("", response_model=CustomPage[RedamOut])
async def listado_redams(
    autoridad_id: int = None,
    distrito_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de deudores"""
    if current_user.permissions.get("REDAMS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_redams(
            db=db,
            autoridad_id=autoridad_id,
            distrito_id=distrito_id,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@redams.get("/{redam_id}", response_model=OneRedamOut)
async def detalle_redam(
    redam_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una deudores a partir de su id"""
    if current_user.permissions.get("REDAMS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        redam = get_redam(
            db=db,
            redam_id=redam_id,
        )
    except PWAnyError as error:
        return OneRedamOut(success=False, message=str(error))
    return OneRedamOut.from_orm(redam)
