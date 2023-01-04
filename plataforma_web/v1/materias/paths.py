"""
Materias v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

from .crud import get_materias, get_materia
from .schemas import MateriaOut, OneMateriaOut

materias = APIRouter(prefix="/v1/materias", tags=["catalogos"])


@materias.get("", response_model=CustomPage[MateriaOut])
async def listado_materias(
    estatus: str = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de materias"""
    if current_user.permissions.get("MATERIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_materias(
            db=db,
            estatus=estatus,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@materias.get("/{materia_id}", response_model=OneMateriaOut)
async def detalle_materia(
    materia_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una materia a partir de su id"""
    if current_user.permissions.get("MATERIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        materia = get_materia(
            db=db,
            materia_id=materia_id,
        )
    except PWAnyError as error:
        return OneMateriaOut(success=False, message=str(error))
    return OneMateriaOut.from_orm(materia)
