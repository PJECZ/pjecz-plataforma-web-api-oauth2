"""
Permisos v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_permisos, get_permiso
from .models import Permiso
from .schemas import PermisoOut, OnePermisoOut
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

permisos = APIRouter(prefix="/v1/permisos", tags=["usuarios"])


@permisos.get("", response_model=CustomPage[PermisoOut])
async def listado_permisos(
    modulo_id: int = None,
    rol_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de permisos"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_permisos(
            db=db,
            modulo_id=modulo_id,
            rol_id=rol_id,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@permisos.get("/{permiso_id}", response_model=OnePermisoOut)
async def detalle_permiso(
    permiso_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una permiso a partir de su id"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        permiso = get_permiso(
            db=db,
            permiso_id=permiso_id,
        )
    except PWAnyError as error:
        return OnePermisoOut(success=False, message=str(error))
    return OnePermisoOut.from_orm(permiso)
