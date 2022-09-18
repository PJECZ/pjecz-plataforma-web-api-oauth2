"""
Oficinas v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_oficinas, get_oficina
from .schemas import OficinaOut, OneOficinaOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

oficinas = APIRouter(prefix="/v1/oficinas", tags=["catalogos"])


@oficinas.get("", response_model=CustomPage[OficinaOut])
async def listado_oficinas(
    distrito_id: int = None,
    domicilio_id: int = None,
    es_juridicional: bool = False,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de oficinas"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_oficinas(
            db,
            distrito_id=distrito_id,
            domicilio_id=domicilio_id,
            es_jurisdiccional=es_juridicional,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@oficinas.get("/{oficina_id}", response_model=OneOficinaOut)
async def detalle_oficina(
    oficina_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una oficina a partir de su id"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        oficina = get_oficina(
            db,
            oficina_id=oficina_id,
        )
    except PWAnyError as error:
        return OneOficinaOut(success=False, message=str(error))
    return OneOficinaOut.from_orm(oficina)
