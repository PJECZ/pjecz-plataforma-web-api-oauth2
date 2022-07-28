"""
Abogados v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException, OutOfRangeException
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.abogados.crud import get_abogados, get_abogado
from plataforma_web.v1.abogados.schemas import AbogadoOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

abogados = APIRouter(prefix="/v1/abogados", tags=["abogados"])


@abogados.get("", response_model=LimitOffsetPage[AbogadoOut])
async def listado_abogados(
    anio_desde: int = None,
    anio_hasta: int = None,
    nombre: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de abogados"""
    if current_user.permissions.get("ABOGADOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_abogados(
            db,
            anio_desde=anio_desde,
            anio_hasta=anio_hasta,
            nombre=nombre,
        )
    except (IsDeletedException, NotExistsException, OutOfRangeException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@abogados.get("/{abogado_id}", response_model=AbogadoOut)
async def detalle_abogado(
    abogado_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una abogados a partir de su id"""
    if current_user.permissions.get("ABOGADOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        abogado = get_abogado(
            db,
            abogado_id=abogado_id,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return AbogadoOut.from_orm(abogado)
