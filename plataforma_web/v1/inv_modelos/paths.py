"""
Inventarios Modelos v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PlataformaWebAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_inv_modelos, get_inv_modelo
from .schemas import InvModeloOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

inv_modelos = APIRouter(prefix="/v1/inv_modelos", tags=["inventarios"])


@inv_modelos.get("", response_model=LimitOffsetPage[InvModeloOut])
async def listado_inv_modelos(
    inv_marca_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de modelos"""
    if current_user.permissions.get("INV MODELOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_inv_modelos(
            db,
            inv_marca_id=inv_marca_id,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@inv_modelos.get("/{inv_modelo_id}", response_model=InvModeloOut)
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
            db,
            inv_modelo_id=inv_modelo_id,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return InvModeloOut.from_orm(inv_modelo)
