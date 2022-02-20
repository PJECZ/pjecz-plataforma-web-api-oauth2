"""
Domicilios v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from plataforma_web.v1.domicilios.crud import get_domicilios, get_domicilio
from plataforma_web.v1.domicilios.schemas import DomicilioOut
from plataforma_web.v1.permisos.models import Permiso
from plataforma_web.v1.usuarios.authentications import get_current_active_user
from plataforma_web.v1.usuarios.schemas import UsuarioInDB

domicilios = APIRouter(prefix="/v1/domicilios", tags=["usuarios"])


@domicilios.get("", response_model=LimitOffsetPage[DomicilioOut])
async def listado_domicilios(
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de domicilios"""
    if "domicilio" not in current_user.permissions or current_user.permissions["domicilio"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_domicilios(db))


@domicilios.get("/{domicilio_id}", response_model=DomicilioOut)
async def detalle_domicilio(
    domicilio_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una domicilio a partir de su id"""
    if "domicilio" not in current_user.permissions or current_user.permissions["domicilio"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        domicilio = get_domicilio(db, domicilio_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return DomicilioOut.from_orm(domicilio)
