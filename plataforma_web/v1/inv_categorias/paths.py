"""
Inventarios Categorias v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_inv_categoria, get_inv_categorias
from .schemas import InvCategoriaOut, OneInvCategoriaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

inv_categorias = APIRouter(prefix="/v1/inv_categorias", tags=["inventarios"])


@inv_categorias.get("", response_model=CustomPage[InvCategoriaOut])
async def listado_inv_categorias(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de categorias"""
    if current_user.permissions.get("INV CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_inv_categorias(db)
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@inv_categorias.get("/{inv_categoria_id}", response_model=OneInvCategoriaOut)
async def detalle_inv_categoria(
    inv_categoria_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una categorias a partir de su id"""
    if current_user.permissions.get("INV CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_categoria = get_inv_categoria(
            db,
            inv_categoria_id=inv_categoria_id,
        )
    except PWAnyError as error:
        return OneInvCategoriaOut(success=False, message=str(error))
    return OneInvCategoriaOut.from_orm(inv_categoria)
