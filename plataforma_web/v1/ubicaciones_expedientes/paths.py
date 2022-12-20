"""
Ubicaciones Expedientes v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_ubicaciones_expedientes, get_ubicacion_expediente
from .schemas import UbicacionExpedienteOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

ubicaciones_expedientes = APIRouter(prefix="/v1/ubicaciones_expedientes", tags=["ubicaciones expedientes"])


@ubicaciones_expedientes.get("", response_model=CustomPage[UbicacionExpedienteOut])
async def listado_ubicaciones_expedientes(
    autoridad_id: int = None,
    autoridad_clave: str = None,
    expediente: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de ubicacion de expedientes"""
    if current_user.permissions.get("UBICACIONES EXPEDIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_ubicaciones_expedientes(
            db=db,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            expediente=expediente,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@ubicaciones_expedientes.get("/{ubicacion_expediente_id}", response_model=UbicacionExpedienteOut)
async def detalle_ubicacion_expediente(
    ubicacion_expediente_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una ubicacion de expediente a partir de su id"""
    if current_user.permissions.get("UBICACIONES EXPEDIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        ubicacion_expediente = get_ubicacion_expediente(db, ubicacion_expediente_id=ubicacion_expediente_id)
    except PWAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return UbicacionExpedienteOut.from_orm(ubicacion_expediente)
