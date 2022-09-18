"""
Autoridades v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_autoridad, get_autoridades
from .schemas import AutoridadOut, OneAutoridadOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

autoridades = APIRouter(prefix="/v1/autoridades", tags=["catalogos"])


@autoridades.get("", response_model=CustomPage[AutoridadOut])
async def listado_autoridades(
    distrito_id: int = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    materia_id: int = None,
    organo_jurisdiccional: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de autoridades"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_autoridades(
            db,
            distrito_id=distrito_id,
            es_jurisdiccional=es_jurisdiccional,
            es_notaria=es_notaria,
            materia_id=materia_id,
            organo_jurisdiccional=organo_jurisdiccional,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(listado)


@autoridades.get("/{autoridad_id}", response_model=OneAutoridadOut)
async def detalle_autoridad(
    autoridad_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una autoridad a partir de su clave"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        autoridad = get_autoridad(
            db,
            autoridad_id=autoridad_id,
        )
    except PWAnyError as error:
        return OneAutoridadOut(success=False, message=str(error))
    return OneAutoridadOut.from_orm(autoridad)
