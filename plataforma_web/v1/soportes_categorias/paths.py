"""
Soportes Categorias v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PlataformaWebAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_soportes_categorias, get_soporte_categoria
from .schemas import SoporteCategoriaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

soportes_categorias = APIRouter(prefix="/v1/soportes_categorias", tags=["soportes"])


@soportes_categorias.get("", response_model=LimitOffsetPage[SoporteCategoriaOut])
async def listado_soportes_categorias(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de categorias"""
    if current_user.permissions.get("SOPORTES CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_soportes_categorias(db)
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@soportes_categorias.get("/{soporte_categoria_id}", response_model=SoporteCategoriaOut)
async def detalle_soporte_categoria(
    soporte_categoria_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una categoria a partir de su id"""
    if current_user.permissions.get("SOPORTES CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        soporte_categoria = get_soporte_categoria(
            db,
            soporte_categoria_id=soporte_categoria_id,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return SoporteCategoriaOut.from_orm(soporte_categoria)
