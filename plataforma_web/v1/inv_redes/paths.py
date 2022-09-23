"""
Inevntarios Redes v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_inv_redes, get_inv_red
from .schemas import InvRedOut, OneInvRedOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

inv_redes = APIRouter(prefix="/v1/inv_redes", tags=["inventarios"])


@inv_redes.get("", response_model=CustomPage[InvRedOut])
async def listado_inv_redes(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de redes"""
    if current_user.permissions.get("INV REDES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_inv_redes(db=db)
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@inv_redes.get("/{inv_red_id}", response_model=OneInvRedOut)
async def detalle_inv_red(
    inv_red_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una redes a partir de su id"""
    if current_user.permissions.get("INV REDES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_red = get_inv_red(
            db=db,
            inv_red_id=inv_red_id,
        )
    except PWAnyError as error:
        return OneInvRedOut(success=False, message=str(error))
    return OneInvRedOut.from_orm(inv_red)
