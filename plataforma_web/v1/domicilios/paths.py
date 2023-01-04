"""
Domicilios v1, rutas (paths)
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

from .crud import get_domicilios, get_domicilio
from .schemas import DomicilioOut, OneDomicilioOut

domicilios = APIRouter(prefix="/v1/domicilios", tags=["catalogos"])


@domicilios.get("", response_model=CustomPage[DomicilioOut])
async def listado_domicilios(
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de domicilios"""
    if current_user.permissions.get("DOMICILIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_domicilios(
            db=db,
            estatus=estatus,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@domicilios.get("/{domicilio_id}", response_model=OneDomicilioOut)
async def detalle_domicilio(
    domicilio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una domicilio a partir de su id"""
    if current_user.permissions.get("DOMICILIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        domicilio = get_domicilio(
            db=db,
            domicilio_id=domicilio_id,
        )
    except PWAnyError as error:
        return OneDomicilioOut(success=False, message=str(error))
    return OneDomicilioOut.from_orm(domicilio)
