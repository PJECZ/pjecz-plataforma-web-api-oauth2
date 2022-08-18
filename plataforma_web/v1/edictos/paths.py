"""
Edictos v1, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PlataformaWebAnyError
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.edictos.crud import get_edictos, get_edicto
from plataforma_web.v1.edictos.schemas import EdictoOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

edictos = APIRouter(prefix="/v1/edictos", tags=["edictos"])


@edictos.get("", response_model=LimitOffsetPage[EdictoOut])
async def listado_edictos(
    autoridad_id: int = None,
    fecha: date = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de edictos"""
    if current_user.permissions.get("EDICTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_edictos(
            db,
            autoridad_id=autoridad_id,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@edictos.get("/{edicto_id}", response_model=EdictoOut)
async def detalle_edicto(
    edicto_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una edictos a partir de su id"""
    if current_user.permissions.get("EDICTOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        edicto = get_edicto(db, edicto_id=edicto_id)
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EdictoOut.from_orm(edicto)
