"""
Centros de Trabajo v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.centros_trabajos.crud import get_centro_trabajo, get_centro_trabajo_from_clave, get_centros_trabajos
from plataforma_web.v1.centros_trabajos.schemas import CentroTrabajoOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

centros_trabajos = APIRouter(prefix="/v1/centros_trabajos", tags=["funcionarios"])


@centros_trabajos.get("", response_model=LimitOffsetPage[CentroTrabajoOut])
async def listado_centros_trabajos(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de centros de trabajo"""
    if "CENTROS TRABAJOS" not in current_user.permissions or current_user.permissions["CENTROS TRABAJOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_centros_trabajos(db))


@centros_trabajos.get("/{centro_trabajo_id}", response_model=CentroTrabajoOut)
async def detalle_centro_trabajo(
    centro_trabajo_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un centro de trabajo a partir de su clave"""
    if "CENTROS TRABAJOS" not in current_user.permissions or current_user.permissions["CENTROS TRABAJOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        centro_trabajo = get_centro_trabajo(db, centro_trabajo_id=centro_trabajo_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CentroTrabajoOut.from_orm(centro_trabajo)
