"""
Soportes Categorias v1, rutas (paths)
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

from .crud import get_soportes_categorias, get_soporte_categoria
from .schemas import SoporteCategoriaOut, OneSoporteCategoriaOut

soportes_categorias = APIRouter(prefix="/v1/soportes_categorias", tags=["soportes"])


@soportes_categorias.get("", response_model=CustomPage[SoporteCategoriaOut])
async def listado_soportes_categorias(
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de categorias"""
    if current_user.permissions.get("SOPORTES CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_soportes_categorias(
            db=db,
            estatus=estatus,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@soportes_categorias.get("/{soporte_categoria_id}", response_model=OneSoporteCategoriaOut)
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
            db=db,
            soporte_categoria_id=soporte_categoria_id,
        )
    except PWAnyError as error:
        return OneSoporteCategoriaOut(success=False, message=str(error))
    return OneSoporteCategoriaOut.from_orm(soporte_categoria)
