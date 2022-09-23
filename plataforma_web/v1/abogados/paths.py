"""
Abogados v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_abogados, get_abogado
from .schemas import AbogadoOut, OneAbogadoOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

abogados = APIRouter(prefix="/v1/abogados", tags=["abogados"])


@abogados.get("", response_model=CustomPage[AbogadoOut])
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
        consulta = get_abogados(
            db=db,
            anio_desde=anio_desde,
            anio_hasta=anio_hasta,
            nombre=nombre,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@abogados.get("/{abogado_id}", response_model=OneAbogadoOut)
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
            db=db,
            abogado_id=abogado_id,
        )
    except PWAnyError as error:
        return OneAbogadoOut(success=False, message=str(error))
    return OneAbogadoOut.from_orm(abogado)
