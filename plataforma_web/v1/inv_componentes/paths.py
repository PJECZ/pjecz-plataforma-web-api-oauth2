"""
Inventarios Componentes v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import PlataformaWebAnyError
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_inv_componente, get_inv_componentes
from .schemas import InvComponenteOut
from ..permisos.models import Permiso
from ..usuarios.authentications import get_current_active_user
from ..usuarios.schemas import UsuarioInDB

inv_componentes = APIRouter(prefix="/v1/inv_componentes", tags=["inventarios"])


@inv_componentes.get("", response_model=LimitOffsetPage[InvComponenteOut])
async def listado_inv_componentes(
    inv_categoria_id: int = None,
    inv_equipo_id: int = None,
    generacion: str = False,
    current_user: UsuarioInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de componentes"""
    if current_user.permissions.get("INV COMPONENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_inv_componentes(
            db,
            inv_categoria_id=inv_categoria_id,
            inv_equipo_id=inv_equipo_id,
            generacion=generacion,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@inv_componentes.get("/{inv_componente_id}", response_model=InvComponenteOut)
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
            db,
            inv_componente_id=inv_componente_id,
        )
    except PlataformaWebAnyError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return InvComponenteOut.from_orm(inv_componente)
