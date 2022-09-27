"""
Inventarios Marcas v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_inv_marcas, get_inv_marca
from .schemas import InvMarcaOut, OneInvMarcaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

inv_marcas = APIRouter(prefix="/v1/inv_marcas", tags=["inventarios"])


@inv_marcas.get("", response_model=CustomPage[InvMarcaOut])
async def listado_inv_marcas(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de marcas"""
    if current_user.permissions.get("INV MARCAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_inv_marcas(db=db)
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@inv_marcas.get("/{inv_marca_id}", response_model=OneInvMarcaOut)
async def detalle_inv_marca(
    inv_marca_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una marcas a partir de su id"""
    if current_user.permissions.get("INV MARCAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_marca = get_inv_marca(
            db=db,
            inv_marca_id=inv_marca_id,
        )
    except PWAnyError as error:
        return OneInvMarcaOut(success=False, message=str(error))
    return OneInvMarcaOut.from_orm(inv_marca)
