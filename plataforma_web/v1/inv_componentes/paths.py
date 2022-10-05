"""
Inventarios Componentes v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PWAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_inv_componente, get_inv_componentes
from .schemas import InvComponenteOut, OneInvComponenteOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

inv_componentes = APIRouter(prefix="/v1/inv_componentes", tags=["inventarios"])


@inv_componentes.get("", response_model=CustomPage[InvComponenteOut])
async def listado_inv_componentes(
    generacion: str = None,
    inv_categoria_id: int = None,
    inv_equipo_id: int = None,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de componentes"""
    if current_user.permissions.get("INV COMPONENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        consulta = get_inv_componentes(
            db=db,
            generacion=generacion,
            inv_categoria_id=inv_categoria_id,
            inv_equipo_id=inv_equipo_id,
        )
    except PWAnyError as error:
        return custom_page_success_false(error)
    return paginate(consulta)


@inv_componentes.get("/{inv_componente_id}", response_model=OneInvComponenteOut)
async def detalle_inv_componente(
    inv_componente_id: int,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una componentes a partir de su id"""
    if current_user.permissions.get("INV COMPONENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        inv_componente = get_inv_componente(
            db=db,
            inv_componente_id=inv_componente_id,
        )
    except PWAnyError as error:
        return OneInvComponenteOut(success=False, message=str(error))
    return OneInvComponenteOut.from_orm(inv_componente)
