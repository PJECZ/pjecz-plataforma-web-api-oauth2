"""
Inventarios Modelos v1, rutas (paths)
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

from .crud import get_inv_modelos, get_inv_modelo
from .schemas import InvModeloOut, OneInvModeloOut

inv_modelos = APIRouter(prefix="/v1/inv_modelos", tags=["inventarios"])


@inv_modelos.get("", response_model=CustomPage[InvModeloOut])
async def listado_inv_modelos(
    estatus: str = None,
    inv_marca_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de modelos"""
    if current_user.permissions.get("INV MODELOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_inv_modelos(
            db=db,
            estatus=estatus,
            inv_marca_id=inv_marca_id,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@inv_modelos.get("/{inv_modelo_id}", response_model=OneInvModeloOut)
async def detalle_inv_modelo(
    inv_modelo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una modelos a partir de su id"""
    if current_user.permissions.get("INV MODELOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_modelo = get_inv_modelo(
            db=db,
            inv_modelo_id=inv_modelo_id,
        )
    except PWAnyError as error:
        return OneInvModeloOut(success=False, message=str(error))
    return OneInvModeloOut.from_orm(inv_modelo)
