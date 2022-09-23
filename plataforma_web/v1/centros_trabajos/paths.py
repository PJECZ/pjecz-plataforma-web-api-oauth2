"""
Centros de Trabajo v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_centro_trabajo, get_centros_trabajos
from .schemas import CentroTrabajoOut, OneCentroTrabajoOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

centros_trabajos = APIRouter(prefix="/v1/centros_trabajos", tags=["funcionarios"])


@centros_trabajos.get("", response_model=CustomPage[CentroTrabajoOut])
async def listado_centros_trabajos(
    distrito_id: int = None,
    domicilio_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de centros de trabajo"""
    if current_user.permissions.get("CENTROS TRABAJOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_centros_trabajos(
            db=db,
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@centros_trabajos.get("/{centro_trabajo_id}", response_model=OneCentroTrabajoOut)
async def detalle_centro_trabajo(
    centro_trabajo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un centro de trabajo a partir de su clave"""
    if current_user.permissions.get("CENTROS TRABAJOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        centro_trabajo = get_centro_trabajo(
            db=db,
            centro_trabajo_id=centro_trabajo_id,
        )
    except PWAnyError as error:
        return OneCentroTrabajoOut(success=False, message=str(error))
    return OneCentroTrabajoOut.from_orm(centro_trabajo)
