"""
Inventarios Custodias v1, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_inv_custodia, get_inv_custodias
from .schemas import InvCustodiaOut, OneInvCustodiaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

inv_custodias = APIRouter(prefix="/v1/inv_custodias", tags=["inventarios"])


@inv_custodias.get("", response_model=CustomPage[InvCustodiaOut])
async def listado_inv_custodias(
    usuario_id: int = None,
    usuario_email: str = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de custodias"""
    if current_user.permissions.get("INV CUSTODIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_inv_custodias(
            db,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@inv_custodias.get("/{inv_custodia_id}", response_model=OneInvCustodiaOut)
async def detalle_inv_custodia(
    inv_custodia_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una custodias a partir de su id"""
    if current_user.permissions.get("INV CUSTODIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_custodia = get_inv_custodia(
            db,
            inv_custodia_id=inv_custodia_id,
        )
    except PWAnyError as error:
        return OneInvCustodiaOut(success=False, message=str(error))
    return OneInvCustodiaOut.from_orm(inv_custodia)
