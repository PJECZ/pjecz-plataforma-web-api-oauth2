"""
Edictos v1, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_edictos, get_edicto
from .schemas import EdictoOut, OneEdictoOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

edictos = APIRouter(prefix="/v1/edictos", tags=["edictos"])


@edictos.get("", response_model=CustomPage[EdictoOut])
async def listado_edictos(
    autoridad_id: int = None,
    autoridad_clave: str = None,
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
            autoridad_clave=autoridad_clave,
            fecha=fecha,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@edictos.get("/{edicto_id}", response_model=OneEdictoOut)
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
    except PWAnyError as error:
        return OneEdictoOut(success=False, message=str(error))
    return OneEdictoOut.from_orm(edicto)
