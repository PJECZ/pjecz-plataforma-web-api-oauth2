"""
Centros de Trabajo v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PlataformaWebAnyError
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.centros_trabajos.crud import get_centro_trabajo, get_centros_trabajos
from plataforma_web.v1.centros_trabajos.schemas import CentroTrabajoOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

centros_trabajos = APIRouter(prefix="/v1/centros_trabajos", tags=["funcionarios"])


@centros_trabajos.get("", response_model=LimitOffsetPage[CentroTrabajoOut])
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
        listado = get_centros_trabajos(
            db,
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@centros_trabajos.get("/{centro_trabajo_id}", response_model=CentroTrabajoOut)
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
            db,
            centro_trabajo_id=centro_trabajo_id,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CentroTrabajoOut.from_orm(centro_trabajo)
