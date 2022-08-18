"""
Inventarios Marcas v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PlataformaWebAnyError
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.inv_marcas.crud import get_inv_marcas, get_inv_marca
from plataforma_web.v1.inv_marcas.schemas import InvMarcaOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

inv_marcas = APIRouter(prefix="/v1/inv_marcas", tags=["inventarios"])


@inv_marcas.get("", response_model=LimitOffsetPage[InvMarcaOut])
async def listado_inv_marcas(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de marcas"""
    if current_user.permissions.get("INV MARCAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_inv_marcas(db)
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@inv_marcas.get("/{inv_marca_id}", response_model=InvMarcaOut)
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
            db,
            inv_marca_id=inv_marca_id,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return InvMarcaOut.from_orm(inv_marca)
