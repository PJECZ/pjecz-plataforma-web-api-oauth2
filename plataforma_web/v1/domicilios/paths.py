"""
Domicilios v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import IsDeletedException, NotExistsException
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.domicilios.crud import get_domicilios, get_domicilio
from plataforma_web.v1.domicilios.schemas import DomicilioOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

domicilios = APIRouter(prefix="/v1/domicilios", tags=["oficinas"])


@domicilios.get("", response_model=LimitOffsetPage[DomicilioOut])
async def listado_domicilios(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de domicilios"""
    if "DOMICILIOS" not in current_user.permissions or current_user.permissions["DOMICILIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_domicilios(db)
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@domicilios.get("/{domicilio_id}", response_model=DomicilioOut)
async def detalle_domicilio(
    domicilio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una domicilio a partir de su id"""
    if "DOMICILIOS" not in current_user.permissions or current_user.permissions["DOMICILIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        domicilio = get_domicilio(
            db,
            domicilio_id=domicilio_id,
        )
    except (IsDeletedException, NotExistsException) as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return DomicilioOut.from_orm(domicilio)
